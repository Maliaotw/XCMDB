import logging

from django.db.models.fields.related import ForeignKey

def diff_models_field(fields, obj1, obj2):
    ret = []
    for key in fields:
        if str(getattr(obj1, key)) != str(getattr(obj2, key)):
            ret.append(key)
    return ret


def get_models_field(model):
    # model = getattr(cls)
    ret = []
    f = model._meta.fields
    for i in f:
        key = i.attname

        if key in ['id', 'last_date','create_at','latest_date']:
            continue

        if issubclass(type(i), ForeignKey):
            key = key.replace('_id', '')

        ret.append(key)

    return ret


def create_one(models_class, data, filter_field={}):
    '''

    retrun: {
        'code':1,
        'message':'',
        'obj':''
    }

    code 1 新增 ,2 更新,3 沒有變化
    '''

    result = {
        'code':0,
        'message':'',
        'obj':''
    }


    instance_obj = models_class.objects.filter(**filter_field)
    logging.debug("{} {}".format(instance_obj, data))


    fields = get_models_field(models_class)
    ins_data = {i: data.get(i) for i in fields}

    if instance_obj:
        # 存在時 比較差異
        instance_obj = instance_obj.first()
        instance_obj2 = models_class(**ins_data)

        # 比較差異
        ret = diff_models_field(fields, instance_obj, instance_obj2)
        if ret:
            # 有差異則更新
            for i in ret:
                before_val = getattr(instance_obj,i)
                setattr(instance_obj, i, ins_data[i])
                instance_obj.save()
                result['code'] = 2
                result['message'] = '更新 %s (字段: "%s" %s -> %s)' % (instance_obj,i ,before_val,ins_data[i])
        else:
            result['code'] = 3
            result['message'] = '沒有變化'


    else:
        # 不存在新增
        instance_obj = models_class.objects.create(**ins_data)
        result['code'] = 1
        result['message'] = '新增 %s' % instance_obj

    result['obj'] = instance_obj

    return result


if __name__ == '__main__':
    pass


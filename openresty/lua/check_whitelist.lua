local iputils = require("resty.iputils")
iputils.enable_lrucache()

function file_exists(file)
  local f = io.open(file, "rb")
  if f then f:close() end
  return f ~= nil
end

function lines_from(file)
  if not file_exists(file) then return {} end

  lines = {}
  for line in io.lines(file) do
    lines[#lines + 1] = line
  end

  return lines
end

local file = "/etc/nginx/whitelist.conf"
local whitelist_ips = lines_from(file)
local whitelist = iputils.parse_cidrs(whitelist_ips)


if not iputils.ip_in_cidrs(ngx.var.remote_addr, whitelist) then
   return ngx.exit(ngx.HTTP_FORBIDDEN)
end

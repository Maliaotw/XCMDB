rocks_trees = {
   { name = "user", root = home .. "/.luarocks" };
   { name = "system", root = "/usr/local" };
}
lua_interpreter = "luajit";
variables = {
   LUA_DIR = "/usr/local/openresty/luajit";
   LUA_BINDIR = "/usr/local/openresty/luajit/bin";
   LUA_LIBDIR = "/usr/local/openresty/luajit/lib",
}
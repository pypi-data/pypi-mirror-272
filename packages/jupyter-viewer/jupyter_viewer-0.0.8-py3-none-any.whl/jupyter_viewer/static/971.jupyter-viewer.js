"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[971],{

/***/ 93907:
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {



var __values = this && this.__values || function (o) {
  var s = typeof Symbol === "function" && Symbol.iterator,
    m = s && o[s],
    i = 0;
  if (m) return m.call(o);
  if (o && typeof o.length === "number") return {
    next: function () {
      if (o && i >= o.length) o = void 0;
      return {
        value: o && o[i++],
        done: !o
      };
    }
  };
  throw new TypeError(s ? "Object is not iterable." : "Symbol.iterator is not defined.");
};
Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports.MathJax = exports.combineWithMathJax = exports.combineDefaults = exports.combineConfig = exports.isObject = void 0;
var version_js_1 = __webpack_require__(184);
function isObject(x) {
  return typeof x === 'object' && x !== null;
}
exports.isObject = isObject;
function combineConfig(dst, src) {
  var e_1, _a;
  try {
    for (var _b = __values(Object.keys(src)), _c = _b.next(); !_c.done; _c = _b.next()) {
      var id = _c.value;
      if (id === '__esModule') continue;
      if (isObject(dst[id]) && isObject(src[id]) && !(src[id] instanceof Promise)) {
        combineConfig(dst[id], src[id]);
      } else if (src[id] !== null && src[id] !== undefined) {
        dst[id] = src[id];
      }
    }
  } catch (e_1_1) {
    e_1 = {
      error: e_1_1
    };
  } finally {
    try {
      if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
    } finally {
      if (e_1) throw e_1.error;
    }
  }
  return dst;
}
exports.combineConfig = combineConfig;
function combineDefaults(dst, name, src) {
  var e_2, _a;
  if (!dst[name]) {
    dst[name] = {};
  }
  dst = dst[name];
  try {
    for (var _b = __values(Object.keys(src)), _c = _b.next(); !_c.done; _c = _b.next()) {
      var id = _c.value;
      if (isObject(dst[id]) && isObject(src[id])) {
        combineDefaults(dst, id, src[id]);
      } else if (dst[id] == null && src[id] != null) {
        dst[id] = src[id];
      }
    }
  } catch (e_2_1) {
    e_2 = {
      error: e_2_1
    };
  } finally {
    try {
      if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
    } finally {
      if (e_2) throw e_2.error;
    }
  }
  return dst;
}
exports.combineDefaults = combineDefaults;
function combineWithMathJax(config) {
  return combineConfig(exports.MathJax, config);
}
exports.combineWithMathJax = combineWithMathJax;
if (typeof __webpack_require__.g.MathJax === 'undefined') {
  __webpack_require__.g.MathJax = {};
}
if (!__webpack_require__.g.MathJax.version) {
  __webpack_require__.g.MathJax = {
    version: version_js_1.VERSION,
    _: {},
    config: __webpack_require__.g.MathJax
  };
}
exports.MathJax = __webpack_require__.g.MathJax;

/***/ }),

/***/ 6233:
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

var __dirname = "/";


var __values = this && this.__values || function (o) {
  var s = typeof Symbol === "function" && Symbol.iterator,
    m = s && o[s],
    i = 0;
  if (m) return m.call(o);
  if (o && typeof o.length === "number") return {
    next: function () {
      if (o && i >= o.length) o = void 0;
      return {
        value: o && o[i++],
        done: !o
      };
    }
  };
  throw new TypeError(s ? "Object is not iterable." : "Symbol.iterator is not defined.");
};
var e_1, _a;
Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports.CONFIG = exports.MathJax = exports.Loader = exports.PathFilters = exports.PackageError = exports.Package = void 0;
var global_js_1 = __webpack_require__(93907);
var package_js_1 = __webpack_require__(51173);
var package_js_2 = __webpack_require__(51173);
Object.defineProperty(exports, "Package", ({
  enumerable: true,
  get: function () {
    return package_js_2.Package;
  }
}));
Object.defineProperty(exports, "PackageError", ({
  enumerable: true,
  get: function () {
    return package_js_2.PackageError;
  }
}));
var FunctionList_js_1 = __webpack_require__(58235);
exports.PathFilters = {
  source: function (data) {
    if (exports.CONFIG.source.hasOwnProperty(data.name)) {
      data.name = exports.CONFIG.source[data.name];
    }
    return true;
  },
  normalize: function (data) {
    var name = data.name;
    if (!name.match(/^(?:[a-z]+:\/)?\/|[a-z]:\\|\[/i)) {
      data.name = '[mathjax]/' + name.replace(/^\.\//, '');
    }
    if (data.addExtension && !name.match(/\.[^\/]+$/)) {
      data.name += '.js';
    }
    return true;
  },
  prefix: function (data) {
    var match;
    while (match = data.name.match(/^\[([^\]]*)\]/)) {
      if (!exports.CONFIG.paths.hasOwnProperty(match[1])) break;
      data.name = exports.CONFIG.paths[match[1]] + data.name.substr(match[0].length);
    }
    return true;
  }
};
var Loader;
(function (Loader) {
  var VERSION = global_js_1.MathJax.version;
  Loader.versions = new Map();
  function ready() {
    var e_2, _a;
    var names = [];
    for (var _i = 0; _i < arguments.length; _i++) {
      names[_i] = arguments[_i];
    }
    if (names.length === 0) {
      names = Array.from(package_js_1.Package.packages.keys());
    }
    var promises = [];
    try {
      for (var names_1 = __values(names), names_1_1 = names_1.next(); !names_1_1.done; names_1_1 = names_1.next()) {
        var name_1 = names_1_1.value;
        var extension = package_js_1.Package.packages.get(name_1) || new package_js_1.Package(name_1, true);
        promises.push(extension.promise);
      }
    } catch (e_2_1) {
      e_2 = {
        error: e_2_1
      };
    } finally {
      try {
        if (names_1_1 && !names_1_1.done && (_a = names_1.return)) _a.call(names_1);
      } finally {
        if (e_2) throw e_2.error;
      }
    }
    return Promise.all(promises);
  }
  Loader.ready = ready;
  function load() {
    var e_3, _a;
    var names = [];
    for (var _i = 0; _i < arguments.length; _i++) {
      names[_i] = arguments[_i];
    }
    if (names.length === 0) {
      return Promise.resolve();
    }
    var promises = [];
    var _loop_1 = function (name_2) {
      var extension = package_js_1.Package.packages.get(name_2);
      if (!extension) {
        extension = new package_js_1.Package(name_2);
        extension.provides(exports.CONFIG.provides[name_2]);
      }
      extension.checkNoLoad();
      promises.push(extension.promise.then(function () {
        if (!exports.CONFIG.versionWarnings) return;
        if (extension.isLoaded && !Loader.versions.has(package_js_1.Package.resolvePath(name_2))) {
          console.warn("No version information available for component ".concat(name_2));
        }
      }));
    };
    try {
      for (var names_2 = __values(names), names_2_1 = names_2.next(); !names_2_1.done; names_2_1 = names_2.next()) {
        var name_2 = names_2_1.value;
        _loop_1(name_2);
      }
    } catch (e_3_1) {
      e_3 = {
        error: e_3_1
      };
    } finally {
      try {
        if (names_2_1 && !names_2_1.done && (_a = names_2.return)) _a.call(names_2);
      } finally {
        if (e_3) throw e_3.error;
      }
    }
    package_js_1.Package.loadAll();
    return Promise.all(promises);
  }
  Loader.load = load;
  function preLoad() {
    var e_4, _a;
    var names = [];
    for (var _i = 0; _i < arguments.length; _i++) {
      names[_i] = arguments[_i];
    }
    try {
      for (var names_3 = __values(names), names_3_1 = names_3.next(); !names_3_1.done; names_3_1 = names_3.next()) {
        var name_3 = names_3_1.value;
        var extension = package_js_1.Package.packages.get(name_3);
        if (!extension) {
          extension = new package_js_1.Package(name_3, true);
          extension.provides(exports.CONFIG.provides[name_3]);
        }
        extension.loaded();
      }
    } catch (e_4_1) {
      e_4 = {
        error: e_4_1
      };
    } finally {
      try {
        if (names_3_1 && !names_3_1.done && (_a = names_3.return)) _a.call(names_3);
      } finally {
        if (e_4) throw e_4.error;
      }
    }
  }
  Loader.preLoad = preLoad;
  function defaultReady() {
    if (typeof exports.MathJax.startup !== 'undefined') {
      exports.MathJax.config.startup.ready();
    }
  }
  Loader.defaultReady = defaultReady;
  function getRoot() {
    var root = __dirname + '/../../es5';
    if (typeof document !== 'undefined') {
      var script = document.currentScript || document.getElementById('MathJax-script');
      if (script) {
        root = script.src.replace(/\/[^\/]*$/, '');
      }
    }
    return root;
  }
  Loader.getRoot = getRoot;
  function checkVersion(name, version, _type) {
    Loader.versions.set(package_js_1.Package.resolvePath(name), VERSION);
    if (exports.CONFIG.versionWarnings && version !== VERSION) {
      console.warn("Component ".concat(name, " uses ").concat(version, " of MathJax; version in use is ").concat(VERSION));
      return true;
    }
    return false;
  }
  Loader.checkVersion = checkVersion;
  Loader.pathFilters = new FunctionList_js_1.FunctionList();
  Loader.pathFilters.add(exports.PathFilters.source, 0);
  Loader.pathFilters.add(exports.PathFilters.normalize, 10);
  Loader.pathFilters.add(exports.PathFilters.prefix, 20);
})(Loader = exports.Loader || (exports.Loader = {}));
exports.MathJax = global_js_1.MathJax;
if (typeof exports.MathJax.loader === 'undefined') {
  (0, global_js_1.combineDefaults)(exports.MathJax.config, 'loader', {
    paths: {
      mathjax: Loader.getRoot()
    },
    source: {},
    dependencies: {},
    provides: {},
    load: [],
    ready: Loader.defaultReady.bind(Loader),
    failed: function (error) {
      return console.log("MathJax(".concat(error.package || '?', "): ").concat(error.message));
    },
    require: null,
    pathFilters: [],
    versionWarnings: true
  });
  (0, global_js_1.combineWithMathJax)({
    loader: Loader
  });
  try {
    for (var _b = __values(exports.MathJax.config.loader.pathFilters), _c = _b.next(); !_c.done; _c = _b.next()) {
      var filter = _c.value;
      if (Array.isArray(filter)) {
        Loader.pathFilters.add(filter[0], filter[1]);
      } else {
        Loader.pathFilters.add(filter);
      }
    }
  } catch (e_1_1) {
    e_1 = {
      error: e_1_1
    };
  } finally {
    try {
      if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
    } finally {
      if (e_1) throw e_1.error;
    }
  }
}
exports.CONFIG = exports.MathJax.config.loader;

/***/ }),

/***/ 51173:
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {



var __extends = this && this.__extends || function () {
  var extendStatics = function (d, b) {
    extendStatics = Object.setPrototypeOf || {
      __proto__: []
    } instanceof Array && function (d, b) {
      d.__proto__ = b;
    } || function (d, b) {
      for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p];
    };
    return extendStatics(d, b);
  };
  return function (d, b) {
    if (typeof b !== "function" && b !== null) throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
    extendStatics(d, b);
    function __() {
      this.constructor = d;
    }
    d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
  };
}();
var __values = this && this.__values || function (o) {
  var s = typeof Symbol === "function" && Symbol.iterator,
    m = s && o[s],
    i = 0;
  if (m) return m.call(o);
  if (o && typeof o.length === "number") return {
    next: function () {
      if (o && i >= o.length) o = void 0;
      return {
        value: o && o[i++],
        done: !o
      };
    }
  };
  throw new TypeError(s ? "Object is not iterable." : "Symbol.iterator is not defined.");
};
var __read = this && this.__read || function (o, n) {
  var m = typeof Symbol === "function" && o[Symbol.iterator];
  if (!m) return o;
  var i = m.call(o),
    r,
    ar = [],
    e;
  try {
    while ((n === void 0 || n-- > 0) && !(r = i.next()).done) ar.push(r.value);
  } catch (error) {
    e = {
      error: error
    };
  } finally {
    try {
      if (r && !r.done && (m = i["return"])) m.call(i);
    } finally {
      if (e) throw e.error;
    }
  }
  return ar;
};
var __spreadArray = this && this.__spreadArray || function (to, from, pack) {
  if (pack || arguments.length === 2) for (var i = 0, l = from.length, ar; i < l; i++) {
    if (ar || !(i in from)) {
      if (!ar) ar = Array.prototype.slice.call(from, 0, i);
      ar[i] = from[i];
    }
  }
  return to.concat(ar || Array.prototype.slice.call(from));
};
Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports.Package = exports.PackageError = void 0;
var loader_js_1 = __webpack_require__(6233);
var PackageError = function (_super) {
  __extends(PackageError, _super);
  function PackageError(message, name) {
    var _this = _super.call(this, message) || this;
    _this.package = name;
    return _this;
  }
  return PackageError;
}(Error);
exports.PackageError = PackageError;
var Package = function () {
  function Package(name, noLoad) {
    if (noLoad === void 0) {
      noLoad = false;
    }
    this.isLoaded = false;
    this.isLoading = false;
    this.hasFailed = false;
    this.dependents = [];
    this.dependencies = [];
    this.dependencyCount = 0;
    this.provided = [];
    this.name = name;
    this.noLoad = noLoad;
    Package.packages.set(name, this);
    this.promise = this.makePromise(this.makeDependencies());
  }
  Object.defineProperty(Package.prototype, "canLoad", {
    get: function () {
      return this.dependencyCount === 0 && !this.noLoad && !this.isLoading && !this.hasFailed;
    },
    enumerable: false,
    configurable: true
  });
  Package.resolvePath = function (name, addExtension) {
    if (addExtension === void 0) {
      addExtension = true;
    }
    var data = {
      name: name,
      original: name,
      addExtension: addExtension
    };
    loader_js_1.Loader.pathFilters.execute(data);
    return data.name;
  };
  Package.loadAll = function () {
    var e_1, _a;
    try {
      for (var _b = __values(this.packages.values()), _c = _b.next(); !_c.done; _c = _b.next()) {
        var extension = _c.value;
        if (extension.canLoad) {
          extension.load();
        }
      }
    } catch (e_1_1) {
      e_1 = {
        error: e_1_1
      };
    } finally {
      try {
        if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
      } finally {
        if (e_1) throw e_1.error;
      }
    }
  };
  Package.prototype.makeDependencies = function () {
    var e_2, _a;
    var promises = [];
    var map = Package.packages;
    var noLoad = this.noLoad;
    var name = this.name;
    var dependencies = [];
    if (loader_js_1.CONFIG.dependencies.hasOwnProperty(name)) {
      dependencies.push.apply(dependencies, __spreadArray([], __read(loader_js_1.CONFIG.dependencies[name]), false));
    } else if (name !== 'core') {
      dependencies.push('core');
    }
    try {
      for (var dependencies_1 = __values(dependencies), dependencies_1_1 = dependencies_1.next(); !dependencies_1_1.done; dependencies_1_1 = dependencies_1.next()) {
        var dependent = dependencies_1_1.value;
        var extension = map.get(dependent) || new Package(dependent, noLoad);
        if (this.dependencies.indexOf(extension) < 0) {
          extension.addDependent(this, noLoad);
          this.dependencies.push(extension);
          if (!extension.isLoaded) {
            this.dependencyCount++;
            promises.push(extension.promise);
          }
        }
      }
    } catch (e_2_1) {
      e_2 = {
        error: e_2_1
      };
    } finally {
      try {
        if (dependencies_1_1 && !dependencies_1_1.done && (_a = dependencies_1.return)) _a.call(dependencies_1);
      } finally {
        if (e_2) throw e_2.error;
      }
    }
    return promises;
  };
  Package.prototype.makePromise = function (promises) {
    var _this = this;
    var promise = new Promise(function (resolve, reject) {
      _this.resolve = resolve;
      _this.reject = reject;
    });
    var config = loader_js_1.CONFIG[this.name] || {};
    if (config.ready) {
      promise = promise.then(function (_name) {
        return config.ready(_this.name);
      });
    }
    if (promises.length) {
      promises.push(promise);
      promise = Promise.all(promises).then(function (names) {
        return names.join(', ');
      });
    }
    if (config.failed) {
      promise.catch(function (message) {
        return config.failed(new PackageError(message, _this.name));
      });
    }
    return promise;
  };
  Package.prototype.load = function () {
    if (!this.isLoaded && !this.isLoading && !this.noLoad) {
      this.isLoading = true;
      var url = Package.resolvePath(this.name);
      if (loader_js_1.CONFIG.require) {
        this.loadCustom(url);
      } else {
        this.loadScript(url);
      }
    }
  };
  Package.prototype.loadCustom = function (url) {
    var _this = this;
    try {
      var result = loader_js_1.CONFIG.require(url);
      if (result instanceof Promise) {
        result.then(function () {
          return _this.checkLoad();
        }).catch(function (err) {
          return _this.failed('Can\'t load "' + url + '"\n' + err.message.trim());
        });
      } else {
        this.checkLoad();
      }
    } catch (err) {
      this.failed(err.message);
    }
  };
  Package.prototype.loadScript = function (url) {
    var _this = this;
    var script = document.createElement('script');
    script.src = url;
    script.charset = 'UTF-8';
    script.onload = function (_event) {
      return _this.checkLoad();
    };
    script.onerror = function (_event) {
      return _this.failed('Can\'t load "' + url + '"');
    };
    document.head.appendChild(script);
  };
  Package.prototype.loaded = function () {
    var e_3, _a, e_4, _b;
    this.isLoaded = true;
    this.isLoading = false;
    try {
      for (var _c = __values(this.dependents), _d = _c.next(); !_d.done; _d = _c.next()) {
        var dependent = _d.value;
        dependent.requirementSatisfied();
      }
    } catch (e_3_1) {
      e_3 = {
        error: e_3_1
      };
    } finally {
      try {
        if (_d && !_d.done && (_a = _c.return)) _a.call(_c);
      } finally {
        if (e_3) throw e_3.error;
      }
    }
    try {
      for (var _e = __values(this.provided), _f = _e.next(); !_f.done; _f = _e.next()) {
        var provided = _f.value;
        provided.loaded();
      }
    } catch (e_4_1) {
      e_4 = {
        error: e_4_1
      };
    } finally {
      try {
        if (_f && !_f.done && (_b = _e.return)) _b.call(_e);
      } finally {
        if (e_4) throw e_4.error;
      }
    }
    this.resolve(this.name);
  };
  Package.prototype.failed = function (message) {
    this.hasFailed = true;
    this.isLoading = false;
    this.reject(new PackageError(message, this.name));
  };
  Package.prototype.checkLoad = function () {
    var _this = this;
    var config = loader_js_1.CONFIG[this.name] || {};
    var checkReady = config.checkReady || function () {
      return Promise.resolve();
    };
    checkReady().then(function () {
      return _this.loaded();
    }).catch(function (message) {
      return _this.failed(message);
    });
  };
  Package.prototype.requirementSatisfied = function () {
    if (this.dependencyCount) {
      this.dependencyCount--;
      if (this.canLoad) {
        this.load();
      }
    }
  };
  Package.prototype.provides = function (names) {
    var e_5, _a;
    if (names === void 0) {
      names = [];
    }
    try {
      for (var names_1 = __values(names), names_1_1 = names_1.next(); !names_1_1.done; names_1_1 = names_1.next()) {
        var name_1 = names_1_1.value;
        var provided = Package.packages.get(name_1);
        if (!provided) {
          if (!loader_js_1.CONFIG.dependencies[name_1]) {
            loader_js_1.CONFIG.dependencies[name_1] = [];
          }
          loader_js_1.CONFIG.dependencies[name_1].push(name_1);
          provided = new Package(name_1, true);
          provided.isLoading = true;
        }
        this.provided.push(provided);
      }
    } catch (e_5_1) {
      e_5 = {
        error: e_5_1
      };
    } finally {
      try {
        if (names_1_1 && !names_1_1.done && (_a = names_1.return)) _a.call(names_1);
      } finally {
        if (e_5) throw e_5.error;
      }
    }
  };
  Package.prototype.addDependent = function (extension, noLoad) {
    this.dependents.push(extension);
    if (!noLoad) {
      this.checkNoLoad();
    }
  };
  Package.prototype.checkNoLoad = function () {
    var e_6, _a;
    if (this.noLoad) {
      this.noLoad = false;
      try {
        for (var _b = __values(this.dependencies), _c = _b.next(); !_c.done; _c = _b.next()) {
          var dependency = _c.value;
          dependency.checkNoLoad();
        }
      } catch (e_6_1) {
        e_6 = {
          error: e_6_1
        };
      } finally {
        try {
          if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
        } finally {
          if (e_6) throw e_6.error;
        }
      }
    }
  };
  Package.packages = new Map();
  return Package;
}();
exports.Package = Package;

/***/ }),

/***/ 80971:
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {



var __values = this && this.__values || function (o) {
  var s = typeof Symbol === "function" && Symbol.iterator,
    m = s && o[s],
    i = 0;
  if (m) return m.call(o);
  if (o && typeof o.length === "number") return {
    next: function () {
      if (o && i >= o.length) o = void 0;
      return {
        value: o && o[i++],
        done: !o
      };
    }
  };
  throw new TypeError(s ? "Object is not iterable." : "Symbol.iterator is not defined.");
};
var __read = this && this.__read || function (o, n) {
  var m = typeof Symbol === "function" && o[Symbol.iterator];
  if (!m) return o;
  var i = m.call(o),
    r,
    ar = [],
    e;
  try {
    while ((n === void 0 || n-- > 0) && !(r = i.next()).done) ar.push(r.value);
  } catch (error) {
    e = {
      error: error
    };
  } finally {
    try {
      if (r && !r.done && (m = i["return"])) m.call(i);
    } finally {
      if (e) throw e.error;
    }
  }
  return ar;
};
var __spreadArray = this && this.__spreadArray || function (to, from, pack) {
  if (pack || arguments.length === 2) for (var i = 0, l = from.length, ar; i < l; i++) {
    if (ar || !(i in from)) {
      if (!ar) ar = Array.prototype.slice.call(from, 0, i);
      ar[i] = from[i];
    }
  }
  return to.concat(ar || Array.prototype.slice.call(from));
};
var __importDefault = this && this.__importDefault || function (mod) {
  return mod && mod.__esModule ? mod : {
    "default": mod
  };
};
Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports.RequireConfiguration = exports.options = exports.RequireMethods = exports.RequireLoad = void 0;
var Configuration_js_1 = __webpack_require__(34268);
var SymbolMap_js_1 = __webpack_require__(62117);
var TexError_js_1 = __importDefault(__webpack_require__(19795));
var global_js_1 = __webpack_require__(93907);
var package_js_1 = __webpack_require__(51173);
var loader_js_1 = __webpack_require__(6233);
var mathjax_js_1 = __webpack_require__(63385);
var Options_js_1 = __webpack_require__(62704);
var MJCONFIG = global_js_1.MathJax.config;
function RegisterExtension(jax, name) {
  var _a;
  var require = jax.parseOptions.options.require;
  var required = jax.parseOptions.packageData.get('require').required;
  var extension = name.substr(require.prefix.length);
  if (required.indexOf(extension) < 0) {
    required.push(extension);
    RegisterDependencies(jax, loader_js_1.CONFIG.dependencies[name]);
    var handler = Configuration_js_1.ConfigurationHandler.get(extension);
    if (handler) {
      var options_1 = MJCONFIG[name] || {};
      if (handler.options && Object.keys(handler.options).length === 1 && handler.options[extension]) {
        options_1 = (_a = {}, _a[extension] = options_1, _a);
      }
      jax.configuration.add(extension, jax, options_1);
      var configured = jax.parseOptions.packageData.get('require').configured;
      if (handler.preprocessors.length && !configured.has(extension)) {
        configured.set(extension, true);
        mathjax_js_1.mathjax.retryAfter(Promise.resolve());
      }
    }
  }
}
function RegisterDependencies(jax, names) {
  var e_1, _a;
  if (names === void 0) {
    names = [];
  }
  var prefix = jax.parseOptions.options.require.prefix;
  try {
    for (var names_1 = __values(names), names_1_1 = names_1.next(); !names_1_1.done; names_1_1 = names_1.next()) {
      var name_1 = names_1_1.value;
      if (name_1.substr(0, prefix.length) === prefix) {
        RegisterExtension(jax, name_1);
      }
    }
  } catch (e_1_1) {
    e_1 = {
      error: e_1_1
    };
  } finally {
    try {
      if (names_1_1 && !names_1_1.done && (_a = names_1.return)) _a.call(names_1);
    } finally {
      if (e_1) throw e_1.error;
    }
  }
}
function RequireLoad(parser, name) {
  var options = parser.options.require;
  var allow = options.allow;
  var extension = (name.substr(0, 1) === '[' ? '' : options.prefix) + name;
  var allowed = allow.hasOwnProperty(extension) ? allow[extension] : allow.hasOwnProperty(name) ? allow[name] : options.defaultAllow;
  if (!allowed) {
    throw new TexError_js_1.default('BadRequire', 'Extension "%1" is not allowed to be loaded', extension);
  }
  if (package_js_1.Package.packages.has(extension)) {
    RegisterExtension(parser.configuration.packageData.get('require').jax, extension);
  } else {
    mathjax_js_1.mathjax.retryAfter(loader_js_1.Loader.load(extension));
  }
}
exports.RequireLoad = RequireLoad;
function config(_config, jax) {
  jax.parseOptions.packageData.set('require', {
    jax: jax,
    required: __spreadArray([], __read(jax.options.packages), false),
    configured: new Map()
  });
  var options = jax.parseOptions.options.require;
  var prefix = options.prefix;
  if (prefix.match(/[^_a-zA-Z0-9]/)) {
    throw Error('Illegal characters used in \\require prefix');
  }
  if (!loader_js_1.CONFIG.paths[prefix]) {
    loader_js_1.CONFIG.paths[prefix] = '[mathjax]/input/tex/extensions';
  }
  options.prefix = '[' + prefix + ']/';
}
exports.RequireMethods = {
  Require: function (parser, name) {
    var required = parser.GetArgument(name);
    if (required.match(/[^_a-zA-Z0-9]/) || required === '') {
      throw new TexError_js_1.default('BadPackageName', 'Argument for %1 is not a valid package name', name);
    }
    RequireLoad(parser, required);
  }
};
exports.options = {
  require: {
    allow: (0, Options_js_1.expandable)({
      base: false,
      'all-packages': false,
      autoload: false,
      configmacros: false,
      tagformat: false,
      setoptions: false
    }),
    defaultAllow: true,
    prefix: 'tex'
  }
};
new SymbolMap_js_1.CommandMap('require', {
  require: 'Require'
}, exports.RequireMethods);
exports.RequireConfiguration = Configuration_js_1.Configuration.create('require', {
  handler: {
    macro: ['require']
  },
  config: config,
  options: exports.options
});

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiOTcxLmp1cHl0ZXItdmlld2VyLmpzIiwibWFwcGluZ3MiOiI7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOzs7Ozs7OztBQ2hHQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7Ozs7Ozs7QUNyUEE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7Ozs7OztBQ2xYQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vQGRhdGFsYXllci9qdXB5dGVyLXZpZXdlci8uL25vZGVfbW9kdWxlcy9tYXRoamF4LWZ1bGwvanMvY29tcG9uZW50cy9nbG9iYWwuanMiLCJ3ZWJwYWNrOi8vQGRhdGFsYXllci9qdXB5dGVyLXZpZXdlci8uL25vZGVfbW9kdWxlcy9tYXRoamF4LWZ1bGwvanMvY29tcG9uZW50cy9sb2FkZXIuanMiLCJ3ZWJwYWNrOi8vQGRhdGFsYXllci9qdXB5dGVyLXZpZXdlci8uL25vZGVfbW9kdWxlcy9tYXRoamF4LWZ1bGwvanMvY29tcG9uZW50cy9wYWNrYWdlLmpzIiwid2VicGFjazovL0BkYXRhbGF5ZXIvanVweXRlci12aWV3ZXIvLi9ub2RlX21vZHVsZXMvbWF0aGpheC1mdWxsL2pzL2lucHV0L3RleC9yZXF1aXJlL1JlcXVpcmVDb25maWd1cmF0aW9uLmpzIl0sInNvdXJjZXNDb250ZW50IjpbIlwidXNlIHN0cmljdFwiO1xuXG52YXIgX192YWx1ZXMgPSB0aGlzICYmIHRoaXMuX192YWx1ZXMgfHwgZnVuY3Rpb24gKG8pIHtcbiAgdmFyIHMgPSB0eXBlb2YgU3ltYm9sID09PSBcImZ1bmN0aW9uXCIgJiYgU3ltYm9sLml0ZXJhdG9yLFxuICAgIG0gPSBzICYmIG9bc10sXG4gICAgaSA9IDA7XG4gIGlmIChtKSByZXR1cm4gbS5jYWxsKG8pO1xuICBpZiAobyAmJiB0eXBlb2Ygby5sZW5ndGggPT09IFwibnVtYmVyXCIpIHJldHVybiB7XG4gICAgbmV4dDogZnVuY3Rpb24gKCkge1xuICAgICAgaWYgKG8gJiYgaSA+PSBvLmxlbmd0aCkgbyA9IHZvaWQgMDtcbiAgICAgIHJldHVybiB7XG4gICAgICAgIHZhbHVlOiBvICYmIG9baSsrXSxcbiAgICAgICAgZG9uZTogIW9cbiAgICAgIH07XG4gICAgfVxuICB9O1xuICB0aHJvdyBuZXcgVHlwZUVycm9yKHMgPyBcIk9iamVjdCBpcyBub3QgaXRlcmFibGUuXCIgOiBcIlN5bWJvbC5pdGVyYXRvciBpcyBub3QgZGVmaW5lZC5cIik7XG59O1xuT2JqZWN0LmRlZmluZVByb3BlcnR5KGV4cG9ydHMsIFwiX19lc01vZHVsZVwiLCB7XG4gIHZhbHVlOiB0cnVlXG59KTtcbmV4cG9ydHMuTWF0aEpheCA9IGV4cG9ydHMuY29tYmluZVdpdGhNYXRoSmF4ID0gZXhwb3J0cy5jb21iaW5lRGVmYXVsdHMgPSBleHBvcnRzLmNvbWJpbmVDb25maWcgPSBleHBvcnRzLmlzT2JqZWN0ID0gdm9pZCAwO1xudmFyIHZlcnNpb25fanNfMSA9IHJlcXVpcmUoXCIuL3ZlcnNpb24uanNcIik7XG5mdW5jdGlvbiBpc09iamVjdCh4KSB7XG4gIHJldHVybiB0eXBlb2YgeCA9PT0gJ29iamVjdCcgJiYgeCAhPT0gbnVsbDtcbn1cbmV4cG9ydHMuaXNPYmplY3QgPSBpc09iamVjdDtcbmZ1bmN0aW9uIGNvbWJpbmVDb25maWcoZHN0LCBzcmMpIHtcbiAgdmFyIGVfMSwgX2E7XG4gIHRyeSB7XG4gICAgZm9yICh2YXIgX2IgPSBfX3ZhbHVlcyhPYmplY3Qua2V5cyhzcmMpKSwgX2MgPSBfYi5uZXh0KCk7ICFfYy5kb25lOyBfYyA9IF9iLm5leHQoKSkge1xuICAgICAgdmFyIGlkID0gX2MudmFsdWU7XG4gICAgICBpZiAoaWQgPT09ICdfX2VzTW9kdWxlJykgY29udGludWU7XG4gICAgICBpZiAoaXNPYmplY3QoZHN0W2lkXSkgJiYgaXNPYmplY3Qoc3JjW2lkXSkgJiYgIShzcmNbaWRdIGluc3RhbmNlb2YgUHJvbWlzZSkpIHtcbiAgICAgICAgY29tYmluZUNvbmZpZyhkc3RbaWRdLCBzcmNbaWRdKTtcbiAgICAgIH0gZWxzZSBpZiAoc3JjW2lkXSAhPT0gbnVsbCAmJiBzcmNbaWRdICE9PSB1bmRlZmluZWQpIHtcbiAgICAgICAgZHN0W2lkXSA9IHNyY1tpZF07XG4gICAgICB9XG4gICAgfVxuICB9IGNhdGNoIChlXzFfMSkge1xuICAgIGVfMSA9IHtcbiAgICAgIGVycm9yOiBlXzFfMVxuICAgIH07XG4gIH0gZmluYWxseSB7XG4gICAgdHJ5IHtcbiAgICAgIGlmIChfYyAmJiAhX2MuZG9uZSAmJiAoX2EgPSBfYi5yZXR1cm4pKSBfYS5jYWxsKF9iKTtcbiAgICB9IGZpbmFsbHkge1xuICAgICAgaWYgKGVfMSkgdGhyb3cgZV8xLmVycm9yO1xuICAgIH1cbiAgfVxuICByZXR1cm4gZHN0O1xufVxuZXhwb3J0cy5jb21iaW5lQ29uZmlnID0gY29tYmluZUNvbmZpZztcbmZ1bmN0aW9uIGNvbWJpbmVEZWZhdWx0cyhkc3QsIG5hbWUsIHNyYykge1xuICB2YXIgZV8yLCBfYTtcbiAgaWYgKCFkc3RbbmFtZV0pIHtcbiAgICBkc3RbbmFtZV0gPSB7fTtcbiAgfVxuICBkc3QgPSBkc3RbbmFtZV07XG4gIHRyeSB7XG4gICAgZm9yICh2YXIgX2IgPSBfX3ZhbHVlcyhPYmplY3Qua2V5cyhzcmMpKSwgX2MgPSBfYi5uZXh0KCk7ICFfYy5kb25lOyBfYyA9IF9iLm5leHQoKSkge1xuICAgICAgdmFyIGlkID0gX2MudmFsdWU7XG4gICAgICBpZiAoaXNPYmplY3QoZHN0W2lkXSkgJiYgaXNPYmplY3Qoc3JjW2lkXSkpIHtcbiAgICAgICAgY29tYmluZURlZmF1bHRzKGRzdCwgaWQsIHNyY1tpZF0pO1xuICAgICAgfSBlbHNlIGlmIChkc3RbaWRdID09IG51bGwgJiYgc3JjW2lkXSAhPSBudWxsKSB7XG4gICAgICAgIGRzdFtpZF0gPSBzcmNbaWRdO1xuICAgICAgfVxuICAgIH1cbiAgfSBjYXRjaCAoZV8yXzEpIHtcbiAgICBlXzIgPSB7XG4gICAgICBlcnJvcjogZV8yXzFcbiAgICB9O1xuICB9IGZpbmFsbHkge1xuICAgIHRyeSB7XG4gICAgICBpZiAoX2MgJiYgIV9jLmRvbmUgJiYgKF9hID0gX2IucmV0dXJuKSkgX2EuY2FsbChfYik7XG4gICAgfSBmaW5hbGx5IHtcbiAgICAgIGlmIChlXzIpIHRocm93IGVfMi5lcnJvcjtcbiAgICB9XG4gIH1cbiAgcmV0dXJuIGRzdDtcbn1cbmV4cG9ydHMuY29tYmluZURlZmF1bHRzID0gY29tYmluZURlZmF1bHRzO1xuZnVuY3Rpb24gY29tYmluZVdpdGhNYXRoSmF4KGNvbmZpZykge1xuICByZXR1cm4gY29tYmluZUNvbmZpZyhleHBvcnRzLk1hdGhKYXgsIGNvbmZpZyk7XG59XG5leHBvcnRzLmNvbWJpbmVXaXRoTWF0aEpheCA9IGNvbWJpbmVXaXRoTWF0aEpheDtcbmlmICh0eXBlb2YgZ2xvYmFsLk1hdGhKYXggPT09ICd1bmRlZmluZWQnKSB7XG4gIGdsb2JhbC5NYXRoSmF4ID0ge307XG59XG5pZiAoIWdsb2JhbC5NYXRoSmF4LnZlcnNpb24pIHtcbiAgZ2xvYmFsLk1hdGhKYXggPSB7XG4gICAgdmVyc2lvbjogdmVyc2lvbl9qc18xLlZFUlNJT04sXG4gICAgXzoge30sXG4gICAgY29uZmlnOiBnbG9iYWwuTWF0aEpheFxuICB9O1xufVxuZXhwb3J0cy5NYXRoSmF4ID0gZ2xvYmFsLk1hdGhKYXg7IiwiXCJ1c2Ugc3RyaWN0XCI7XG5cbnZhciBfX3ZhbHVlcyA9IHRoaXMgJiYgdGhpcy5fX3ZhbHVlcyB8fCBmdW5jdGlvbiAobykge1xuICB2YXIgcyA9IHR5cGVvZiBTeW1ib2wgPT09IFwiZnVuY3Rpb25cIiAmJiBTeW1ib2wuaXRlcmF0b3IsXG4gICAgbSA9IHMgJiYgb1tzXSxcbiAgICBpID0gMDtcbiAgaWYgKG0pIHJldHVybiBtLmNhbGwobyk7XG4gIGlmIChvICYmIHR5cGVvZiBvLmxlbmd0aCA9PT0gXCJudW1iZXJcIikgcmV0dXJuIHtcbiAgICBuZXh0OiBmdW5jdGlvbiAoKSB7XG4gICAgICBpZiAobyAmJiBpID49IG8ubGVuZ3RoKSBvID0gdm9pZCAwO1xuICAgICAgcmV0dXJuIHtcbiAgICAgICAgdmFsdWU6IG8gJiYgb1tpKytdLFxuICAgICAgICBkb25lOiAhb1xuICAgICAgfTtcbiAgICB9XG4gIH07XG4gIHRocm93IG5ldyBUeXBlRXJyb3IocyA/IFwiT2JqZWN0IGlzIG5vdCBpdGVyYWJsZS5cIiA6IFwiU3ltYm9sLml0ZXJhdG9yIGlzIG5vdCBkZWZpbmVkLlwiKTtcbn07XG52YXIgZV8xLCBfYTtcbk9iamVjdC5kZWZpbmVQcm9wZXJ0eShleHBvcnRzLCBcIl9fZXNNb2R1bGVcIiwge1xuICB2YWx1ZTogdHJ1ZVxufSk7XG5leHBvcnRzLkNPTkZJRyA9IGV4cG9ydHMuTWF0aEpheCA9IGV4cG9ydHMuTG9hZGVyID0gZXhwb3J0cy5QYXRoRmlsdGVycyA9IGV4cG9ydHMuUGFja2FnZUVycm9yID0gZXhwb3J0cy5QYWNrYWdlID0gdm9pZCAwO1xudmFyIGdsb2JhbF9qc18xID0gcmVxdWlyZShcIi4vZ2xvYmFsLmpzXCIpO1xudmFyIHBhY2thZ2VfanNfMSA9IHJlcXVpcmUoXCIuL3BhY2thZ2UuanNcIik7XG52YXIgcGFja2FnZV9qc18yID0gcmVxdWlyZShcIi4vcGFja2FnZS5qc1wiKTtcbk9iamVjdC5kZWZpbmVQcm9wZXJ0eShleHBvcnRzLCBcIlBhY2thZ2VcIiwge1xuICBlbnVtZXJhYmxlOiB0cnVlLFxuICBnZXQ6IGZ1bmN0aW9uICgpIHtcbiAgICByZXR1cm4gcGFja2FnZV9qc18yLlBhY2thZ2U7XG4gIH1cbn0pO1xuT2JqZWN0LmRlZmluZVByb3BlcnR5KGV4cG9ydHMsIFwiUGFja2FnZUVycm9yXCIsIHtcbiAgZW51bWVyYWJsZTogdHJ1ZSxcbiAgZ2V0OiBmdW5jdGlvbiAoKSB7XG4gICAgcmV0dXJuIHBhY2thZ2VfanNfMi5QYWNrYWdlRXJyb3I7XG4gIH1cbn0pO1xudmFyIEZ1bmN0aW9uTGlzdF9qc18xID0gcmVxdWlyZShcIi4uL3V0aWwvRnVuY3Rpb25MaXN0LmpzXCIpO1xuZXhwb3J0cy5QYXRoRmlsdGVycyA9IHtcbiAgc291cmNlOiBmdW5jdGlvbiAoZGF0YSkge1xuICAgIGlmIChleHBvcnRzLkNPTkZJRy5zb3VyY2UuaGFzT3duUHJvcGVydHkoZGF0YS5uYW1lKSkge1xuICAgICAgZGF0YS5uYW1lID0gZXhwb3J0cy5DT05GSUcuc291cmNlW2RhdGEubmFtZV07XG4gICAgfVxuICAgIHJldHVybiB0cnVlO1xuICB9LFxuICBub3JtYWxpemU6IGZ1bmN0aW9uIChkYXRhKSB7XG4gICAgdmFyIG5hbWUgPSBkYXRhLm5hbWU7XG4gICAgaWYgKCFuYW1lLm1hdGNoKC9eKD86W2Etel0rOlxcLyk/XFwvfFthLXpdOlxcXFx8XFxbL2kpKSB7XG4gICAgICBkYXRhLm5hbWUgPSAnW21hdGhqYXhdLycgKyBuYW1lLnJlcGxhY2UoL15cXC5cXC8vLCAnJyk7XG4gICAgfVxuICAgIGlmIChkYXRhLmFkZEV4dGVuc2lvbiAmJiAhbmFtZS5tYXRjaCgvXFwuW15cXC9dKyQvKSkge1xuICAgICAgZGF0YS5uYW1lICs9ICcuanMnO1xuICAgIH1cbiAgICByZXR1cm4gdHJ1ZTtcbiAgfSxcbiAgcHJlZml4OiBmdW5jdGlvbiAoZGF0YSkge1xuICAgIHZhciBtYXRjaDtcbiAgICB3aGlsZSAobWF0Y2ggPSBkYXRhLm5hbWUubWF0Y2goL15cXFsoW15cXF1dKilcXF0vKSkge1xuICAgICAgaWYgKCFleHBvcnRzLkNPTkZJRy5wYXRocy5oYXNPd25Qcm9wZXJ0eShtYXRjaFsxXSkpIGJyZWFrO1xuICAgICAgZGF0YS5uYW1lID0gZXhwb3J0cy5DT05GSUcucGF0aHNbbWF0Y2hbMV1dICsgZGF0YS5uYW1lLnN1YnN0cihtYXRjaFswXS5sZW5ndGgpO1xuICAgIH1cbiAgICByZXR1cm4gdHJ1ZTtcbiAgfVxufTtcbnZhciBMb2FkZXI7XG4oZnVuY3Rpb24gKExvYWRlcikge1xuICB2YXIgVkVSU0lPTiA9IGdsb2JhbF9qc18xLk1hdGhKYXgudmVyc2lvbjtcbiAgTG9hZGVyLnZlcnNpb25zID0gbmV3IE1hcCgpO1xuICBmdW5jdGlvbiByZWFkeSgpIHtcbiAgICB2YXIgZV8yLCBfYTtcbiAgICB2YXIgbmFtZXMgPSBbXTtcbiAgICBmb3IgKHZhciBfaSA9IDA7IF9pIDwgYXJndW1lbnRzLmxlbmd0aDsgX2krKykge1xuICAgICAgbmFtZXNbX2ldID0gYXJndW1lbnRzW19pXTtcbiAgICB9XG4gICAgaWYgKG5hbWVzLmxlbmd0aCA9PT0gMCkge1xuICAgICAgbmFtZXMgPSBBcnJheS5mcm9tKHBhY2thZ2VfanNfMS5QYWNrYWdlLnBhY2thZ2VzLmtleXMoKSk7XG4gICAgfVxuICAgIHZhciBwcm9taXNlcyA9IFtdO1xuICAgIHRyeSB7XG4gICAgICBmb3IgKHZhciBuYW1lc18xID0gX192YWx1ZXMobmFtZXMpLCBuYW1lc18xXzEgPSBuYW1lc18xLm5leHQoKTsgIW5hbWVzXzFfMS5kb25lOyBuYW1lc18xXzEgPSBuYW1lc18xLm5leHQoKSkge1xuICAgICAgICB2YXIgbmFtZV8xID0gbmFtZXNfMV8xLnZhbHVlO1xuICAgICAgICB2YXIgZXh0ZW5zaW9uID0gcGFja2FnZV9qc18xLlBhY2thZ2UucGFja2FnZXMuZ2V0KG5hbWVfMSkgfHwgbmV3IHBhY2thZ2VfanNfMS5QYWNrYWdlKG5hbWVfMSwgdHJ1ZSk7XG4gICAgICAgIHByb21pc2VzLnB1c2goZXh0ZW5zaW9uLnByb21pc2UpO1xuICAgICAgfVxuICAgIH0gY2F0Y2ggKGVfMl8xKSB7XG4gICAgICBlXzIgPSB7XG4gICAgICAgIGVycm9yOiBlXzJfMVxuICAgICAgfTtcbiAgICB9IGZpbmFsbHkge1xuICAgICAgdHJ5IHtcbiAgICAgICAgaWYgKG5hbWVzXzFfMSAmJiAhbmFtZXNfMV8xLmRvbmUgJiYgKF9hID0gbmFtZXNfMS5yZXR1cm4pKSBfYS5jYWxsKG5hbWVzXzEpO1xuICAgICAgfSBmaW5hbGx5IHtcbiAgICAgICAgaWYgKGVfMikgdGhyb3cgZV8yLmVycm9yO1xuICAgICAgfVxuICAgIH1cbiAgICByZXR1cm4gUHJvbWlzZS5hbGwocHJvbWlzZXMpO1xuICB9XG4gIExvYWRlci5yZWFkeSA9IHJlYWR5O1xuICBmdW5jdGlvbiBsb2FkKCkge1xuICAgIHZhciBlXzMsIF9hO1xuICAgIHZhciBuYW1lcyA9IFtdO1xuICAgIGZvciAodmFyIF9pID0gMDsgX2kgPCBhcmd1bWVudHMubGVuZ3RoOyBfaSsrKSB7XG4gICAgICBuYW1lc1tfaV0gPSBhcmd1bWVudHNbX2ldO1xuICAgIH1cbiAgICBpZiAobmFtZXMubGVuZ3RoID09PSAwKSB7XG4gICAgICByZXR1cm4gUHJvbWlzZS5yZXNvbHZlKCk7XG4gICAgfVxuICAgIHZhciBwcm9taXNlcyA9IFtdO1xuICAgIHZhciBfbG9vcF8xID0gZnVuY3Rpb24gKG5hbWVfMikge1xuICAgICAgdmFyIGV4dGVuc2lvbiA9IHBhY2thZ2VfanNfMS5QYWNrYWdlLnBhY2thZ2VzLmdldChuYW1lXzIpO1xuICAgICAgaWYgKCFleHRlbnNpb24pIHtcbiAgICAgICAgZXh0ZW5zaW9uID0gbmV3IHBhY2thZ2VfanNfMS5QYWNrYWdlKG5hbWVfMik7XG4gICAgICAgIGV4dGVuc2lvbi5wcm92aWRlcyhleHBvcnRzLkNPTkZJRy5wcm92aWRlc1tuYW1lXzJdKTtcbiAgICAgIH1cbiAgICAgIGV4dGVuc2lvbi5jaGVja05vTG9hZCgpO1xuICAgICAgcHJvbWlzZXMucHVzaChleHRlbnNpb24ucHJvbWlzZS50aGVuKGZ1bmN0aW9uICgpIHtcbiAgICAgICAgaWYgKCFleHBvcnRzLkNPTkZJRy52ZXJzaW9uV2FybmluZ3MpIHJldHVybjtcbiAgICAgICAgaWYgKGV4dGVuc2lvbi5pc0xvYWRlZCAmJiAhTG9hZGVyLnZlcnNpb25zLmhhcyhwYWNrYWdlX2pzXzEuUGFja2FnZS5yZXNvbHZlUGF0aChuYW1lXzIpKSkge1xuICAgICAgICAgIGNvbnNvbGUud2FybihcIk5vIHZlcnNpb24gaW5mb3JtYXRpb24gYXZhaWxhYmxlIGZvciBjb21wb25lbnQgXCIuY29uY2F0KG5hbWVfMikpO1xuICAgICAgICB9XG4gICAgICB9KSk7XG4gICAgfTtcbiAgICB0cnkge1xuICAgICAgZm9yICh2YXIgbmFtZXNfMiA9IF9fdmFsdWVzKG5hbWVzKSwgbmFtZXNfMl8xID0gbmFtZXNfMi5uZXh0KCk7ICFuYW1lc18yXzEuZG9uZTsgbmFtZXNfMl8xID0gbmFtZXNfMi5uZXh0KCkpIHtcbiAgICAgICAgdmFyIG5hbWVfMiA9IG5hbWVzXzJfMS52YWx1ZTtcbiAgICAgICAgX2xvb3BfMShuYW1lXzIpO1xuICAgICAgfVxuICAgIH0gY2F0Y2ggKGVfM18xKSB7XG4gICAgICBlXzMgPSB7XG4gICAgICAgIGVycm9yOiBlXzNfMVxuICAgICAgfTtcbiAgICB9IGZpbmFsbHkge1xuICAgICAgdHJ5IHtcbiAgICAgICAgaWYgKG5hbWVzXzJfMSAmJiAhbmFtZXNfMl8xLmRvbmUgJiYgKF9hID0gbmFtZXNfMi5yZXR1cm4pKSBfYS5jYWxsKG5hbWVzXzIpO1xuICAgICAgfSBmaW5hbGx5IHtcbiAgICAgICAgaWYgKGVfMykgdGhyb3cgZV8zLmVycm9yO1xuICAgICAgfVxuICAgIH1cbiAgICBwYWNrYWdlX2pzXzEuUGFja2FnZS5sb2FkQWxsKCk7XG4gICAgcmV0dXJuIFByb21pc2UuYWxsKHByb21pc2VzKTtcbiAgfVxuICBMb2FkZXIubG9hZCA9IGxvYWQ7XG4gIGZ1bmN0aW9uIHByZUxvYWQoKSB7XG4gICAgdmFyIGVfNCwgX2E7XG4gICAgdmFyIG5hbWVzID0gW107XG4gICAgZm9yICh2YXIgX2kgPSAwOyBfaSA8IGFyZ3VtZW50cy5sZW5ndGg7IF9pKyspIHtcbiAgICAgIG5hbWVzW19pXSA9IGFyZ3VtZW50c1tfaV07XG4gICAgfVxuICAgIHRyeSB7XG4gICAgICBmb3IgKHZhciBuYW1lc18zID0gX192YWx1ZXMobmFtZXMpLCBuYW1lc18zXzEgPSBuYW1lc18zLm5leHQoKTsgIW5hbWVzXzNfMS5kb25lOyBuYW1lc18zXzEgPSBuYW1lc18zLm5leHQoKSkge1xuICAgICAgICB2YXIgbmFtZV8zID0gbmFtZXNfM18xLnZhbHVlO1xuICAgICAgICB2YXIgZXh0ZW5zaW9uID0gcGFja2FnZV9qc18xLlBhY2thZ2UucGFja2FnZXMuZ2V0KG5hbWVfMyk7XG4gICAgICAgIGlmICghZXh0ZW5zaW9uKSB7XG4gICAgICAgICAgZXh0ZW5zaW9uID0gbmV3IHBhY2thZ2VfanNfMS5QYWNrYWdlKG5hbWVfMywgdHJ1ZSk7XG4gICAgICAgICAgZXh0ZW5zaW9uLnByb3ZpZGVzKGV4cG9ydHMuQ09ORklHLnByb3ZpZGVzW25hbWVfM10pO1xuICAgICAgICB9XG4gICAgICAgIGV4dGVuc2lvbi5sb2FkZWQoKTtcbiAgICAgIH1cbiAgICB9IGNhdGNoIChlXzRfMSkge1xuICAgICAgZV80ID0ge1xuICAgICAgICBlcnJvcjogZV80XzFcbiAgICAgIH07XG4gICAgfSBmaW5hbGx5IHtcbiAgICAgIHRyeSB7XG4gICAgICAgIGlmIChuYW1lc18zXzEgJiYgIW5hbWVzXzNfMS5kb25lICYmIChfYSA9IG5hbWVzXzMucmV0dXJuKSkgX2EuY2FsbChuYW1lc18zKTtcbiAgICAgIH0gZmluYWxseSB7XG4gICAgICAgIGlmIChlXzQpIHRocm93IGVfNC5lcnJvcjtcbiAgICAgIH1cbiAgICB9XG4gIH1cbiAgTG9hZGVyLnByZUxvYWQgPSBwcmVMb2FkO1xuICBmdW5jdGlvbiBkZWZhdWx0UmVhZHkoKSB7XG4gICAgaWYgKHR5cGVvZiBleHBvcnRzLk1hdGhKYXguc3RhcnR1cCAhPT0gJ3VuZGVmaW5lZCcpIHtcbiAgICAgIGV4cG9ydHMuTWF0aEpheC5jb25maWcuc3RhcnR1cC5yZWFkeSgpO1xuICAgIH1cbiAgfVxuICBMb2FkZXIuZGVmYXVsdFJlYWR5ID0gZGVmYXVsdFJlYWR5O1xuICBmdW5jdGlvbiBnZXRSb290KCkge1xuICAgIHZhciByb290ID0gX19kaXJuYW1lICsgJy8uLi8uLi9lczUnO1xuICAgIGlmICh0eXBlb2YgZG9jdW1lbnQgIT09ICd1bmRlZmluZWQnKSB7XG4gICAgICB2YXIgc2NyaXB0ID0gZG9jdW1lbnQuY3VycmVudFNjcmlwdCB8fCBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgnTWF0aEpheC1zY3JpcHQnKTtcbiAgICAgIGlmIChzY3JpcHQpIHtcbiAgICAgICAgcm9vdCA9IHNjcmlwdC5zcmMucmVwbGFjZSgvXFwvW15cXC9dKiQvLCAnJyk7XG4gICAgICB9XG4gICAgfVxuICAgIHJldHVybiByb290O1xuICB9XG4gIExvYWRlci5nZXRSb290ID0gZ2V0Um9vdDtcbiAgZnVuY3Rpb24gY2hlY2tWZXJzaW9uKG5hbWUsIHZlcnNpb24sIF90eXBlKSB7XG4gICAgTG9hZGVyLnZlcnNpb25zLnNldChwYWNrYWdlX2pzXzEuUGFja2FnZS5yZXNvbHZlUGF0aChuYW1lKSwgVkVSU0lPTik7XG4gICAgaWYgKGV4cG9ydHMuQ09ORklHLnZlcnNpb25XYXJuaW5ncyAmJiB2ZXJzaW9uICE9PSBWRVJTSU9OKSB7XG4gICAgICBjb25zb2xlLndhcm4oXCJDb21wb25lbnQgXCIuY29uY2F0KG5hbWUsIFwiIHVzZXMgXCIpLmNvbmNhdCh2ZXJzaW9uLCBcIiBvZiBNYXRoSmF4OyB2ZXJzaW9uIGluIHVzZSBpcyBcIikuY29uY2F0KFZFUlNJT04pKTtcbiAgICAgIHJldHVybiB0cnVlO1xuICAgIH1cbiAgICByZXR1cm4gZmFsc2U7XG4gIH1cbiAgTG9hZGVyLmNoZWNrVmVyc2lvbiA9IGNoZWNrVmVyc2lvbjtcbiAgTG9hZGVyLnBhdGhGaWx0ZXJzID0gbmV3IEZ1bmN0aW9uTGlzdF9qc18xLkZ1bmN0aW9uTGlzdCgpO1xuICBMb2FkZXIucGF0aEZpbHRlcnMuYWRkKGV4cG9ydHMuUGF0aEZpbHRlcnMuc291cmNlLCAwKTtcbiAgTG9hZGVyLnBhdGhGaWx0ZXJzLmFkZChleHBvcnRzLlBhdGhGaWx0ZXJzLm5vcm1hbGl6ZSwgMTApO1xuICBMb2FkZXIucGF0aEZpbHRlcnMuYWRkKGV4cG9ydHMuUGF0aEZpbHRlcnMucHJlZml4LCAyMCk7XG59KShMb2FkZXIgPSBleHBvcnRzLkxvYWRlciB8fCAoZXhwb3J0cy5Mb2FkZXIgPSB7fSkpO1xuZXhwb3J0cy5NYXRoSmF4ID0gZ2xvYmFsX2pzXzEuTWF0aEpheDtcbmlmICh0eXBlb2YgZXhwb3J0cy5NYXRoSmF4LmxvYWRlciA9PT0gJ3VuZGVmaW5lZCcpIHtcbiAgKDAsIGdsb2JhbF9qc18xLmNvbWJpbmVEZWZhdWx0cykoZXhwb3J0cy5NYXRoSmF4LmNvbmZpZywgJ2xvYWRlcicsIHtcbiAgICBwYXRoczoge1xuICAgICAgbWF0aGpheDogTG9hZGVyLmdldFJvb3QoKVxuICAgIH0sXG4gICAgc291cmNlOiB7fSxcbiAgICBkZXBlbmRlbmNpZXM6IHt9LFxuICAgIHByb3ZpZGVzOiB7fSxcbiAgICBsb2FkOiBbXSxcbiAgICByZWFkeTogTG9hZGVyLmRlZmF1bHRSZWFkeS5iaW5kKExvYWRlciksXG4gICAgZmFpbGVkOiBmdW5jdGlvbiAoZXJyb3IpIHtcbiAgICAgIHJldHVybiBjb25zb2xlLmxvZyhcIk1hdGhKYXgoXCIuY29uY2F0KGVycm9yLnBhY2thZ2UgfHwgJz8nLCBcIik6IFwiKS5jb25jYXQoZXJyb3IubWVzc2FnZSkpO1xuICAgIH0sXG4gICAgcmVxdWlyZTogbnVsbCxcbiAgICBwYXRoRmlsdGVyczogW10sXG4gICAgdmVyc2lvbldhcm5pbmdzOiB0cnVlXG4gIH0pO1xuICAoMCwgZ2xvYmFsX2pzXzEuY29tYmluZVdpdGhNYXRoSmF4KSh7XG4gICAgbG9hZGVyOiBMb2FkZXJcbiAgfSk7XG4gIHRyeSB7XG4gICAgZm9yICh2YXIgX2IgPSBfX3ZhbHVlcyhleHBvcnRzLk1hdGhKYXguY29uZmlnLmxvYWRlci5wYXRoRmlsdGVycyksIF9jID0gX2IubmV4dCgpOyAhX2MuZG9uZTsgX2MgPSBfYi5uZXh0KCkpIHtcbiAgICAgIHZhciBmaWx0ZXIgPSBfYy52YWx1ZTtcbiAgICAgIGlmIChBcnJheS5pc0FycmF5KGZpbHRlcikpIHtcbiAgICAgICAgTG9hZGVyLnBhdGhGaWx0ZXJzLmFkZChmaWx0ZXJbMF0sIGZpbHRlclsxXSk7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICBMb2FkZXIucGF0aEZpbHRlcnMuYWRkKGZpbHRlcik7XG4gICAgICB9XG4gICAgfVxuICB9IGNhdGNoIChlXzFfMSkge1xuICAgIGVfMSA9IHtcbiAgICAgIGVycm9yOiBlXzFfMVxuICAgIH07XG4gIH0gZmluYWxseSB7XG4gICAgdHJ5IHtcbiAgICAgIGlmIChfYyAmJiAhX2MuZG9uZSAmJiAoX2EgPSBfYi5yZXR1cm4pKSBfYS5jYWxsKF9iKTtcbiAgICB9IGZpbmFsbHkge1xuICAgICAgaWYgKGVfMSkgdGhyb3cgZV8xLmVycm9yO1xuICAgIH1cbiAgfVxufVxuZXhwb3J0cy5DT05GSUcgPSBleHBvcnRzLk1hdGhKYXguY29uZmlnLmxvYWRlcjsiLCJcInVzZSBzdHJpY3RcIjtcblxudmFyIF9fZXh0ZW5kcyA9IHRoaXMgJiYgdGhpcy5fX2V4dGVuZHMgfHwgZnVuY3Rpb24gKCkge1xuICB2YXIgZXh0ZW5kU3RhdGljcyA9IGZ1bmN0aW9uIChkLCBiKSB7XG4gICAgZXh0ZW5kU3RhdGljcyA9IE9iamVjdC5zZXRQcm90b3R5cGVPZiB8fCB7XG4gICAgICBfX3Byb3RvX186IFtdXG4gICAgfSBpbnN0YW5jZW9mIEFycmF5ICYmIGZ1bmN0aW9uIChkLCBiKSB7XG4gICAgICBkLl9fcHJvdG9fXyA9IGI7XG4gICAgfSB8fCBmdW5jdGlvbiAoZCwgYikge1xuICAgICAgZm9yICh2YXIgcCBpbiBiKSBpZiAoT2JqZWN0LnByb3RvdHlwZS5oYXNPd25Qcm9wZXJ0eS5jYWxsKGIsIHApKSBkW3BdID0gYltwXTtcbiAgICB9O1xuICAgIHJldHVybiBleHRlbmRTdGF0aWNzKGQsIGIpO1xuICB9O1xuICByZXR1cm4gZnVuY3Rpb24gKGQsIGIpIHtcbiAgICBpZiAodHlwZW9mIGIgIT09IFwiZnVuY3Rpb25cIiAmJiBiICE9PSBudWxsKSB0aHJvdyBuZXcgVHlwZUVycm9yKFwiQ2xhc3MgZXh0ZW5kcyB2YWx1ZSBcIiArIFN0cmluZyhiKSArIFwiIGlzIG5vdCBhIGNvbnN0cnVjdG9yIG9yIG51bGxcIik7XG4gICAgZXh0ZW5kU3RhdGljcyhkLCBiKTtcbiAgICBmdW5jdGlvbiBfXygpIHtcbiAgICAgIHRoaXMuY29uc3RydWN0b3IgPSBkO1xuICAgIH1cbiAgICBkLnByb3RvdHlwZSA9IGIgPT09IG51bGwgPyBPYmplY3QuY3JlYXRlKGIpIDogKF9fLnByb3RvdHlwZSA9IGIucHJvdG90eXBlLCBuZXcgX18oKSk7XG4gIH07XG59KCk7XG52YXIgX192YWx1ZXMgPSB0aGlzICYmIHRoaXMuX192YWx1ZXMgfHwgZnVuY3Rpb24gKG8pIHtcbiAgdmFyIHMgPSB0eXBlb2YgU3ltYm9sID09PSBcImZ1bmN0aW9uXCIgJiYgU3ltYm9sLml0ZXJhdG9yLFxuICAgIG0gPSBzICYmIG9bc10sXG4gICAgaSA9IDA7XG4gIGlmIChtKSByZXR1cm4gbS5jYWxsKG8pO1xuICBpZiAobyAmJiB0eXBlb2Ygby5sZW5ndGggPT09IFwibnVtYmVyXCIpIHJldHVybiB7XG4gICAgbmV4dDogZnVuY3Rpb24gKCkge1xuICAgICAgaWYgKG8gJiYgaSA+PSBvLmxlbmd0aCkgbyA9IHZvaWQgMDtcbiAgICAgIHJldHVybiB7XG4gICAgICAgIHZhbHVlOiBvICYmIG9baSsrXSxcbiAgICAgICAgZG9uZTogIW9cbiAgICAgIH07XG4gICAgfVxuICB9O1xuICB0aHJvdyBuZXcgVHlwZUVycm9yKHMgPyBcIk9iamVjdCBpcyBub3QgaXRlcmFibGUuXCIgOiBcIlN5bWJvbC5pdGVyYXRvciBpcyBub3QgZGVmaW5lZC5cIik7XG59O1xudmFyIF9fcmVhZCA9IHRoaXMgJiYgdGhpcy5fX3JlYWQgfHwgZnVuY3Rpb24gKG8sIG4pIHtcbiAgdmFyIG0gPSB0eXBlb2YgU3ltYm9sID09PSBcImZ1bmN0aW9uXCIgJiYgb1tTeW1ib2wuaXRlcmF0b3JdO1xuICBpZiAoIW0pIHJldHVybiBvO1xuICB2YXIgaSA9IG0uY2FsbChvKSxcbiAgICByLFxuICAgIGFyID0gW10sXG4gICAgZTtcbiAgdHJ5IHtcbiAgICB3aGlsZSAoKG4gPT09IHZvaWQgMCB8fCBuLS0gPiAwKSAmJiAhKHIgPSBpLm5leHQoKSkuZG9uZSkgYXIucHVzaChyLnZhbHVlKTtcbiAgfSBjYXRjaCAoZXJyb3IpIHtcbiAgICBlID0ge1xuICAgICAgZXJyb3I6IGVycm9yXG4gICAgfTtcbiAgfSBmaW5hbGx5IHtcbiAgICB0cnkge1xuICAgICAgaWYgKHIgJiYgIXIuZG9uZSAmJiAobSA9IGlbXCJyZXR1cm5cIl0pKSBtLmNhbGwoaSk7XG4gICAgfSBmaW5hbGx5IHtcbiAgICAgIGlmIChlKSB0aHJvdyBlLmVycm9yO1xuICAgIH1cbiAgfVxuICByZXR1cm4gYXI7XG59O1xudmFyIF9fc3ByZWFkQXJyYXkgPSB0aGlzICYmIHRoaXMuX19zcHJlYWRBcnJheSB8fCBmdW5jdGlvbiAodG8sIGZyb20sIHBhY2spIHtcbiAgaWYgKHBhY2sgfHwgYXJndW1lbnRzLmxlbmd0aCA9PT0gMikgZm9yICh2YXIgaSA9IDAsIGwgPSBmcm9tLmxlbmd0aCwgYXI7IGkgPCBsOyBpKyspIHtcbiAgICBpZiAoYXIgfHwgIShpIGluIGZyb20pKSB7XG4gICAgICBpZiAoIWFyKSBhciA9IEFycmF5LnByb3RvdHlwZS5zbGljZS5jYWxsKGZyb20sIDAsIGkpO1xuICAgICAgYXJbaV0gPSBmcm9tW2ldO1xuICAgIH1cbiAgfVxuICByZXR1cm4gdG8uY29uY2F0KGFyIHx8IEFycmF5LnByb3RvdHlwZS5zbGljZS5jYWxsKGZyb20pKTtcbn07XG5PYmplY3QuZGVmaW5lUHJvcGVydHkoZXhwb3J0cywgXCJfX2VzTW9kdWxlXCIsIHtcbiAgdmFsdWU6IHRydWVcbn0pO1xuZXhwb3J0cy5QYWNrYWdlID0gZXhwb3J0cy5QYWNrYWdlRXJyb3IgPSB2b2lkIDA7XG52YXIgbG9hZGVyX2pzXzEgPSByZXF1aXJlKFwiLi9sb2FkZXIuanNcIik7XG52YXIgUGFja2FnZUVycm9yID0gZnVuY3Rpb24gKF9zdXBlcikge1xuICBfX2V4dGVuZHMoUGFja2FnZUVycm9yLCBfc3VwZXIpO1xuICBmdW5jdGlvbiBQYWNrYWdlRXJyb3IobWVzc2FnZSwgbmFtZSkge1xuICAgIHZhciBfdGhpcyA9IF9zdXBlci5jYWxsKHRoaXMsIG1lc3NhZ2UpIHx8IHRoaXM7XG4gICAgX3RoaXMucGFja2FnZSA9IG5hbWU7XG4gICAgcmV0dXJuIF90aGlzO1xuICB9XG4gIHJldHVybiBQYWNrYWdlRXJyb3I7XG59KEVycm9yKTtcbmV4cG9ydHMuUGFja2FnZUVycm9yID0gUGFja2FnZUVycm9yO1xudmFyIFBhY2thZ2UgPSBmdW5jdGlvbiAoKSB7XG4gIGZ1bmN0aW9uIFBhY2thZ2UobmFtZSwgbm9Mb2FkKSB7XG4gICAgaWYgKG5vTG9hZCA9PT0gdm9pZCAwKSB7XG4gICAgICBub0xvYWQgPSBmYWxzZTtcbiAgICB9XG4gICAgdGhpcy5pc0xvYWRlZCA9IGZhbHNlO1xuICAgIHRoaXMuaXNMb2FkaW5nID0gZmFsc2U7XG4gICAgdGhpcy5oYXNGYWlsZWQgPSBmYWxzZTtcbiAgICB0aGlzLmRlcGVuZGVudHMgPSBbXTtcbiAgICB0aGlzLmRlcGVuZGVuY2llcyA9IFtdO1xuICAgIHRoaXMuZGVwZW5kZW5jeUNvdW50ID0gMDtcbiAgICB0aGlzLnByb3ZpZGVkID0gW107XG4gICAgdGhpcy5uYW1lID0gbmFtZTtcbiAgICB0aGlzLm5vTG9hZCA9IG5vTG9hZDtcbiAgICBQYWNrYWdlLnBhY2thZ2VzLnNldChuYW1lLCB0aGlzKTtcbiAgICB0aGlzLnByb21pc2UgPSB0aGlzLm1ha2VQcm9taXNlKHRoaXMubWFrZURlcGVuZGVuY2llcygpKTtcbiAgfVxuICBPYmplY3QuZGVmaW5lUHJvcGVydHkoUGFja2FnZS5wcm90b3R5cGUsIFwiY2FuTG9hZFwiLCB7XG4gICAgZ2V0OiBmdW5jdGlvbiAoKSB7XG4gICAgICByZXR1cm4gdGhpcy5kZXBlbmRlbmN5Q291bnQgPT09IDAgJiYgIXRoaXMubm9Mb2FkICYmICF0aGlzLmlzTG9hZGluZyAmJiAhdGhpcy5oYXNGYWlsZWQ7XG4gICAgfSxcbiAgICBlbnVtZXJhYmxlOiBmYWxzZSxcbiAgICBjb25maWd1cmFibGU6IHRydWVcbiAgfSk7XG4gIFBhY2thZ2UucmVzb2x2ZVBhdGggPSBmdW5jdGlvbiAobmFtZSwgYWRkRXh0ZW5zaW9uKSB7XG4gICAgaWYgKGFkZEV4dGVuc2lvbiA9PT0gdm9pZCAwKSB7XG4gICAgICBhZGRFeHRlbnNpb24gPSB0cnVlO1xuICAgIH1cbiAgICB2YXIgZGF0YSA9IHtcbiAgICAgIG5hbWU6IG5hbWUsXG4gICAgICBvcmlnaW5hbDogbmFtZSxcbiAgICAgIGFkZEV4dGVuc2lvbjogYWRkRXh0ZW5zaW9uXG4gICAgfTtcbiAgICBsb2FkZXJfanNfMS5Mb2FkZXIucGF0aEZpbHRlcnMuZXhlY3V0ZShkYXRhKTtcbiAgICByZXR1cm4gZGF0YS5uYW1lO1xuICB9O1xuICBQYWNrYWdlLmxvYWRBbGwgPSBmdW5jdGlvbiAoKSB7XG4gICAgdmFyIGVfMSwgX2E7XG4gICAgdHJ5IHtcbiAgICAgIGZvciAodmFyIF9iID0gX192YWx1ZXModGhpcy5wYWNrYWdlcy52YWx1ZXMoKSksIF9jID0gX2IubmV4dCgpOyAhX2MuZG9uZTsgX2MgPSBfYi5uZXh0KCkpIHtcbiAgICAgICAgdmFyIGV4dGVuc2lvbiA9IF9jLnZhbHVlO1xuICAgICAgICBpZiAoZXh0ZW5zaW9uLmNhbkxvYWQpIHtcbiAgICAgICAgICBleHRlbnNpb24ubG9hZCgpO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgfSBjYXRjaCAoZV8xXzEpIHtcbiAgICAgIGVfMSA9IHtcbiAgICAgICAgZXJyb3I6IGVfMV8xXG4gICAgICB9O1xuICAgIH0gZmluYWxseSB7XG4gICAgICB0cnkge1xuICAgICAgICBpZiAoX2MgJiYgIV9jLmRvbmUgJiYgKF9hID0gX2IucmV0dXJuKSkgX2EuY2FsbChfYik7XG4gICAgICB9IGZpbmFsbHkge1xuICAgICAgICBpZiAoZV8xKSB0aHJvdyBlXzEuZXJyb3I7XG4gICAgICB9XG4gICAgfVxuICB9O1xuICBQYWNrYWdlLnByb3RvdHlwZS5tYWtlRGVwZW5kZW5jaWVzID0gZnVuY3Rpb24gKCkge1xuICAgIHZhciBlXzIsIF9hO1xuICAgIHZhciBwcm9taXNlcyA9IFtdO1xuICAgIHZhciBtYXAgPSBQYWNrYWdlLnBhY2thZ2VzO1xuICAgIHZhciBub0xvYWQgPSB0aGlzLm5vTG9hZDtcbiAgICB2YXIgbmFtZSA9IHRoaXMubmFtZTtcbiAgICB2YXIgZGVwZW5kZW5jaWVzID0gW107XG4gICAgaWYgKGxvYWRlcl9qc18xLkNPTkZJRy5kZXBlbmRlbmNpZXMuaGFzT3duUHJvcGVydHkobmFtZSkpIHtcbiAgICAgIGRlcGVuZGVuY2llcy5wdXNoLmFwcGx5KGRlcGVuZGVuY2llcywgX19zcHJlYWRBcnJheShbXSwgX19yZWFkKGxvYWRlcl9qc18xLkNPTkZJRy5kZXBlbmRlbmNpZXNbbmFtZV0pLCBmYWxzZSkpO1xuICAgIH0gZWxzZSBpZiAobmFtZSAhPT0gJ2NvcmUnKSB7XG4gICAgICBkZXBlbmRlbmNpZXMucHVzaCgnY29yZScpO1xuICAgIH1cbiAgICB0cnkge1xuICAgICAgZm9yICh2YXIgZGVwZW5kZW5jaWVzXzEgPSBfX3ZhbHVlcyhkZXBlbmRlbmNpZXMpLCBkZXBlbmRlbmNpZXNfMV8xID0gZGVwZW5kZW5jaWVzXzEubmV4dCgpOyAhZGVwZW5kZW5jaWVzXzFfMS5kb25lOyBkZXBlbmRlbmNpZXNfMV8xID0gZGVwZW5kZW5jaWVzXzEubmV4dCgpKSB7XG4gICAgICAgIHZhciBkZXBlbmRlbnQgPSBkZXBlbmRlbmNpZXNfMV8xLnZhbHVlO1xuICAgICAgICB2YXIgZXh0ZW5zaW9uID0gbWFwLmdldChkZXBlbmRlbnQpIHx8IG5ldyBQYWNrYWdlKGRlcGVuZGVudCwgbm9Mb2FkKTtcbiAgICAgICAgaWYgKHRoaXMuZGVwZW5kZW5jaWVzLmluZGV4T2YoZXh0ZW5zaW9uKSA8IDApIHtcbiAgICAgICAgICBleHRlbnNpb24uYWRkRGVwZW5kZW50KHRoaXMsIG5vTG9hZCk7XG4gICAgICAgICAgdGhpcy5kZXBlbmRlbmNpZXMucHVzaChleHRlbnNpb24pO1xuICAgICAgICAgIGlmICghZXh0ZW5zaW9uLmlzTG9hZGVkKSB7XG4gICAgICAgICAgICB0aGlzLmRlcGVuZGVuY3lDb3VudCsrO1xuICAgICAgICAgICAgcHJvbWlzZXMucHVzaChleHRlbnNpb24ucHJvbWlzZSk7XG4gICAgICAgICAgfVxuICAgICAgICB9XG4gICAgICB9XG4gICAgfSBjYXRjaCAoZV8yXzEpIHtcbiAgICAgIGVfMiA9IHtcbiAgICAgICAgZXJyb3I6IGVfMl8xXG4gICAgICB9O1xuICAgIH0gZmluYWxseSB7XG4gICAgICB0cnkge1xuICAgICAgICBpZiAoZGVwZW5kZW5jaWVzXzFfMSAmJiAhZGVwZW5kZW5jaWVzXzFfMS5kb25lICYmIChfYSA9IGRlcGVuZGVuY2llc18xLnJldHVybikpIF9hLmNhbGwoZGVwZW5kZW5jaWVzXzEpO1xuICAgICAgfSBmaW5hbGx5IHtcbiAgICAgICAgaWYgKGVfMikgdGhyb3cgZV8yLmVycm9yO1xuICAgICAgfVxuICAgIH1cbiAgICByZXR1cm4gcHJvbWlzZXM7XG4gIH07XG4gIFBhY2thZ2UucHJvdG90eXBlLm1ha2VQcm9taXNlID0gZnVuY3Rpb24gKHByb21pc2VzKSB7XG4gICAgdmFyIF90aGlzID0gdGhpcztcbiAgICB2YXIgcHJvbWlzZSA9IG5ldyBQcm9taXNlKGZ1bmN0aW9uIChyZXNvbHZlLCByZWplY3QpIHtcbiAgICAgIF90aGlzLnJlc29sdmUgPSByZXNvbHZlO1xuICAgICAgX3RoaXMucmVqZWN0ID0gcmVqZWN0O1xuICAgIH0pO1xuICAgIHZhciBjb25maWcgPSBsb2FkZXJfanNfMS5DT05GSUdbdGhpcy5uYW1lXSB8fCB7fTtcbiAgICBpZiAoY29uZmlnLnJlYWR5KSB7XG4gICAgICBwcm9taXNlID0gcHJvbWlzZS50aGVuKGZ1bmN0aW9uIChfbmFtZSkge1xuICAgICAgICByZXR1cm4gY29uZmlnLnJlYWR5KF90aGlzLm5hbWUpO1xuICAgICAgfSk7XG4gICAgfVxuICAgIGlmIChwcm9taXNlcy5sZW5ndGgpIHtcbiAgICAgIHByb21pc2VzLnB1c2gocHJvbWlzZSk7XG4gICAgICBwcm9taXNlID0gUHJvbWlzZS5hbGwocHJvbWlzZXMpLnRoZW4oZnVuY3Rpb24gKG5hbWVzKSB7XG4gICAgICAgIHJldHVybiBuYW1lcy5qb2luKCcsICcpO1xuICAgICAgfSk7XG4gICAgfVxuICAgIGlmIChjb25maWcuZmFpbGVkKSB7XG4gICAgICBwcm9taXNlLmNhdGNoKGZ1bmN0aW9uIChtZXNzYWdlKSB7XG4gICAgICAgIHJldHVybiBjb25maWcuZmFpbGVkKG5ldyBQYWNrYWdlRXJyb3IobWVzc2FnZSwgX3RoaXMubmFtZSkpO1xuICAgICAgfSk7XG4gICAgfVxuICAgIHJldHVybiBwcm9taXNlO1xuICB9O1xuICBQYWNrYWdlLnByb3RvdHlwZS5sb2FkID0gZnVuY3Rpb24gKCkge1xuICAgIGlmICghdGhpcy5pc0xvYWRlZCAmJiAhdGhpcy5pc0xvYWRpbmcgJiYgIXRoaXMubm9Mb2FkKSB7XG4gICAgICB0aGlzLmlzTG9hZGluZyA9IHRydWU7XG4gICAgICB2YXIgdXJsID0gUGFja2FnZS5yZXNvbHZlUGF0aCh0aGlzLm5hbWUpO1xuICAgICAgaWYgKGxvYWRlcl9qc18xLkNPTkZJRy5yZXF1aXJlKSB7XG4gICAgICAgIHRoaXMubG9hZEN1c3RvbSh1cmwpO1xuICAgICAgfSBlbHNlIHtcbiAgICAgICAgdGhpcy5sb2FkU2NyaXB0KHVybCk7XG4gICAgICB9XG4gICAgfVxuICB9O1xuICBQYWNrYWdlLnByb3RvdHlwZS5sb2FkQ3VzdG9tID0gZnVuY3Rpb24gKHVybCkge1xuICAgIHZhciBfdGhpcyA9IHRoaXM7XG4gICAgdHJ5IHtcbiAgICAgIHZhciByZXN1bHQgPSBsb2FkZXJfanNfMS5DT05GSUcucmVxdWlyZSh1cmwpO1xuICAgICAgaWYgKHJlc3VsdCBpbnN0YW5jZW9mIFByb21pc2UpIHtcbiAgICAgICAgcmVzdWx0LnRoZW4oZnVuY3Rpb24gKCkge1xuICAgICAgICAgIHJldHVybiBfdGhpcy5jaGVja0xvYWQoKTtcbiAgICAgICAgfSkuY2F0Y2goZnVuY3Rpb24gKGVycikge1xuICAgICAgICAgIHJldHVybiBfdGhpcy5mYWlsZWQoJ0NhblxcJ3QgbG9hZCBcIicgKyB1cmwgKyAnXCJcXG4nICsgZXJyLm1lc3NhZ2UudHJpbSgpKTtcbiAgICAgICAgfSk7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICB0aGlzLmNoZWNrTG9hZCgpO1xuICAgICAgfVxuICAgIH0gY2F0Y2ggKGVycikge1xuICAgICAgdGhpcy5mYWlsZWQoZXJyLm1lc3NhZ2UpO1xuICAgIH1cbiAgfTtcbiAgUGFja2FnZS5wcm90b3R5cGUubG9hZFNjcmlwdCA9IGZ1bmN0aW9uICh1cmwpIHtcbiAgICB2YXIgX3RoaXMgPSB0aGlzO1xuICAgIHZhciBzY3JpcHQgPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KCdzY3JpcHQnKTtcbiAgICBzY3JpcHQuc3JjID0gdXJsO1xuICAgIHNjcmlwdC5jaGFyc2V0ID0gJ1VURi04JztcbiAgICBzY3JpcHQub25sb2FkID0gZnVuY3Rpb24gKF9ldmVudCkge1xuICAgICAgcmV0dXJuIF90aGlzLmNoZWNrTG9hZCgpO1xuICAgIH07XG4gICAgc2NyaXB0Lm9uZXJyb3IgPSBmdW5jdGlvbiAoX2V2ZW50KSB7XG4gICAgICByZXR1cm4gX3RoaXMuZmFpbGVkKCdDYW5cXCd0IGxvYWQgXCInICsgdXJsICsgJ1wiJyk7XG4gICAgfTtcbiAgICBkb2N1bWVudC5oZWFkLmFwcGVuZENoaWxkKHNjcmlwdCk7XG4gIH07XG4gIFBhY2thZ2UucHJvdG90eXBlLmxvYWRlZCA9IGZ1bmN0aW9uICgpIHtcbiAgICB2YXIgZV8zLCBfYSwgZV80LCBfYjtcbiAgICB0aGlzLmlzTG9hZGVkID0gdHJ1ZTtcbiAgICB0aGlzLmlzTG9hZGluZyA9IGZhbHNlO1xuICAgIHRyeSB7XG4gICAgICBmb3IgKHZhciBfYyA9IF9fdmFsdWVzKHRoaXMuZGVwZW5kZW50cyksIF9kID0gX2MubmV4dCgpOyAhX2QuZG9uZTsgX2QgPSBfYy5uZXh0KCkpIHtcbiAgICAgICAgdmFyIGRlcGVuZGVudCA9IF9kLnZhbHVlO1xuICAgICAgICBkZXBlbmRlbnQucmVxdWlyZW1lbnRTYXRpc2ZpZWQoKTtcbiAgICAgIH1cbiAgICB9IGNhdGNoIChlXzNfMSkge1xuICAgICAgZV8zID0ge1xuICAgICAgICBlcnJvcjogZV8zXzFcbiAgICAgIH07XG4gICAgfSBmaW5hbGx5IHtcbiAgICAgIHRyeSB7XG4gICAgICAgIGlmIChfZCAmJiAhX2QuZG9uZSAmJiAoX2EgPSBfYy5yZXR1cm4pKSBfYS5jYWxsKF9jKTtcbiAgICAgIH0gZmluYWxseSB7XG4gICAgICAgIGlmIChlXzMpIHRocm93IGVfMy5lcnJvcjtcbiAgICAgIH1cbiAgICB9XG4gICAgdHJ5IHtcbiAgICAgIGZvciAodmFyIF9lID0gX192YWx1ZXModGhpcy5wcm92aWRlZCksIF9mID0gX2UubmV4dCgpOyAhX2YuZG9uZTsgX2YgPSBfZS5uZXh0KCkpIHtcbiAgICAgICAgdmFyIHByb3ZpZGVkID0gX2YudmFsdWU7XG4gICAgICAgIHByb3ZpZGVkLmxvYWRlZCgpO1xuICAgICAgfVxuICAgIH0gY2F0Y2ggKGVfNF8xKSB7XG4gICAgICBlXzQgPSB7XG4gICAgICAgIGVycm9yOiBlXzRfMVxuICAgICAgfTtcbiAgICB9IGZpbmFsbHkge1xuICAgICAgdHJ5IHtcbiAgICAgICAgaWYgKF9mICYmICFfZi5kb25lICYmIChfYiA9IF9lLnJldHVybikpIF9iLmNhbGwoX2UpO1xuICAgICAgfSBmaW5hbGx5IHtcbiAgICAgICAgaWYgKGVfNCkgdGhyb3cgZV80LmVycm9yO1xuICAgICAgfVxuICAgIH1cbiAgICB0aGlzLnJlc29sdmUodGhpcy5uYW1lKTtcbiAgfTtcbiAgUGFja2FnZS5wcm90b3R5cGUuZmFpbGVkID0gZnVuY3Rpb24gKG1lc3NhZ2UpIHtcbiAgICB0aGlzLmhhc0ZhaWxlZCA9IHRydWU7XG4gICAgdGhpcy5pc0xvYWRpbmcgPSBmYWxzZTtcbiAgICB0aGlzLnJlamVjdChuZXcgUGFja2FnZUVycm9yKG1lc3NhZ2UsIHRoaXMubmFtZSkpO1xuICB9O1xuICBQYWNrYWdlLnByb3RvdHlwZS5jaGVja0xvYWQgPSBmdW5jdGlvbiAoKSB7XG4gICAgdmFyIF90aGlzID0gdGhpcztcbiAgICB2YXIgY29uZmlnID0gbG9hZGVyX2pzXzEuQ09ORklHW3RoaXMubmFtZV0gfHwge307XG4gICAgdmFyIGNoZWNrUmVhZHkgPSBjb25maWcuY2hlY2tSZWFkeSB8fCBmdW5jdGlvbiAoKSB7XG4gICAgICByZXR1cm4gUHJvbWlzZS5yZXNvbHZlKCk7XG4gICAgfTtcbiAgICBjaGVja1JlYWR5KCkudGhlbihmdW5jdGlvbiAoKSB7XG4gICAgICByZXR1cm4gX3RoaXMubG9hZGVkKCk7XG4gICAgfSkuY2F0Y2goZnVuY3Rpb24gKG1lc3NhZ2UpIHtcbiAgICAgIHJldHVybiBfdGhpcy5mYWlsZWQobWVzc2FnZSk7XG4gICAgfSk7XG4gIH07XG4gIFBhY2thZ2UucHJvdG90eXBlLnJlcXVpcmVtZW50U2F0aXNmaWVkID0gZnVuY3Rpb24gKCkge1xuICAgIGlmICh0aGlzLmRlcGVuZGVuY3lDb3VudCkge1xuICAgICAgdGhpcy5kZXBlbmRlbmN5Q291bnQtLTtcbiAgICAgIGlmICh0aGlzLmNhbkxvYWQpIHtcbiAgICAgICAgdGhpcy5sb2FkKCk7XG4gICAgICB9XG4gICAgfVxuICB9O1xuICBQYWNrYWdlLnByb3RvdHlwZS5wcm92aWRlcyA9IGZ1bmN0aW9uIChuYW1lcykge1xuICAgIHZhciBlXzUsIF9hO1xuICAgIGlmIChuYW1lcyA9PT0gdm9pZCAwKSB7XG4gICAgICBuYW1lcyA9IFtdO1xuICAgIH1cbiAgICB0cnkge1xuICAgICAgZm9yICh2YXIgbmFtZXNfMSA9IF9fdmFsdWVzKG5hbWVzKSwgbmFtZXNfMV8xID0gbmFtZXNfMS5uZXh0KCk7ICFuYW1lc18xXzEuZG9uZTsgbmFtZXNfMV8xID0gbmFtZXNfMS5uZXh0KCkpIHtcbiAgICAgICAgdmFyIG5hbWVfMSA9IG5hbWVzXzFfMS52YWx1ZTtcbiAgICAgICAgdmFyIHByb3ZpZGVkID0gUGFja2FnZS5wYWNrYWdlcy5nZXQobmFtZV8xKTtcbiAgICAgICAgaWYgKCFwcm92aWRlZCkge1xuICAgICAgICAgIGlmICghbG9hZGVyX2pzXzEuQ09ORklHLmRlcGVuZGVuY2llc1tuYW1lXzFdKSB7XG4gICAgICAgICAgICBsb2FkZXJfanNfMS5DT05GSUcuZGVwZW5kZW5jaWVzW25hbWVfMV0gPSBbXTtcbiAgICAgICAgICB9XG4gICAgICAgICAgbG9hZGVyX2pzXzEuQ09ORklHLmRlcGVuZGVuY2llc1tuYW1lXzFdLnB1c2gobmFtZV8xKTtcbiAgICAgICAgICBwcm92aWRlZCA9IG5ldyBQYWNrYWdlKG5hbWVfMSwgdHJ1ZSk7XG4gICAgICAgICAgcHJvdmlkZWQuaXNMb2FkaW5nID0gdHJ1ZTtcbiAgICAgICAgfVxuICAgICAgICB0aGlzLnByb3ZpZGVkLnB1c2gocHJvdmlkZWQpO1xuICAgICAgfVxuICAgIH0gY2F0Y2ggKGVfNV8xKSB7XG4gICAgICBlXzUgPSB7XG4gICAgICAgIGVycm9yOiBlXzVfMVxuICAgICAgfTtcbiAgICB9IGZpbmFsbHkge1xuICAgICAgdHJ5IHtcbiAgICAgICAgaWYgKG5hbWVzXzFfMSAmJiAhbmFtZXNfMV8xLmRvbmUgJiYgKF9hID0gbmFtZXNfMS5yZXR1cm4pKSBfYS5jYWxsKG5hbWVzXzEpO1xuICAgICAgfSBmaW5hbGx5IHtcbiAgICAgICAgaWYgKGVfNSkgdGhyb3cgZV81LmVycm9yO1xuICAgICAgfVxuICAgIH1cbiAgfTtcbiAgUGFja2FnZS5wcm90b3R5cGUuYWRkRGVwZW5kZW50ID0gZnVuY3Rpb24gKGV4dGVuc2lvbiwgbm9Mb2FkKSB7XG4gICAgdGhpcy5kZXBlbmRlbnRzLnB1c2goZXh0ZW5zaW9uKTtcbiAgICBpZiAoIW5vTG9hZCkge1xuICAgICAgdGhpcy5jaGVja05vTG9hZCgpO1xuICAgIH1cbiAgfTtcbiAgUGFja2FnZS5wcm90b3R5cGUuY2hlY2tOb0xvYWQgPSBmdW5jdGlvbiAoKSB7XG4gICAgdmFyIGVfNiwgX2E7XG4gICAgaWYgKHRoaXMubm9Mb2FkKSB7XG4gICAgICB0aGlzLm5vTG9hZCA9IGZhbHNlO1xuICAgICAgdHJ5IHtcbiAgICAgICAgZm9yICh2YXIgX2IgPSBfX3ZhbHVlcyh0aGlzLmRlcGVuZGVuY2llcyksIF9jID0gX2IubmV4dCgpOyAhX2MuZG9uZTsgX2MgPSBfYi5uZXh0KCkpIHtcbiAgICAgICAgICB2YXIgZGVwZW5kZW5jeSA9IF9jLnZhbHVlO1xuICAgICAgICAgIGRlcGVuZGVuY3kuY2hlY2tOb0xvYWQoKTtcbiAgICAgICAgfVxuICAgICAgfSBjYXRjaCAoZV82XzEpIHtcbiAgICAgICAgZV82ID0ge1xuICAgICAgICAgIGVycm9yOiBlXzZfMVxuICAgICAgICB9O1xuICAgICAgfSBmaW5hbGx5IHtcbiAgICAgICAgdHJ5IHtcbiAgICAgICAgICBpZiAoX2MgJiYgIV9jLmRvbmUgJiYgKF9hID0gX2IucmV0dXJuKSkgX2EuY2FsbChfYik7XG4gICAgICAgIH0gZmluYWxseSB7XG4gICAgICAgICAgaWYgKGVfNikgdGhyb3cgZV82LmVycm9yO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgfVxuICB9O1xuICBQYWNrYWdlLnBhY2thZ2VzID0gbmV3IE1hcCgpO1xuICByZXR1cm4gUGFja2FnZTtcbn0oKTtcbmV4cG9ydHMuUGFja2FnZSA9IFBhY2thZ2U7IiwiXCJ1c2Ugc3RyaWN0XCI7XG5cbnZhciBfX3ZhbHVlcyA9IHRoaXMgJiYgdGhpcy5fX3ZhbHVlcyB8fCBmdW5jdGlvbiAobykge1xuICB2YXIgcyA9IHR5cGVvZiBTeW1ib2wgPT09IFwiZnVuY3Rpb25cIiAmJiBTeW1ib2wuaXRlcmF0b3IsXG4gICAgbSA9IHMgJiYgb1tzXSxcbiAgICBpID0gMDtcbiAgaWYgKG0pIHJldHVybiBtLmNhbGwobyk7XG4gIGlmIChvICYmIHR5cGVvZiBvLmxlbmd0aCA9PT0gXCJudW1iZXJcIikgcmV0dXJuIHtcbiAgICBuZXh0OiBmdW5jdGlvbiAoKSB7XG4gICAgICBpZiAobyAmJiBpID49IG8ubGVuZ3RoKSBvID0gdm9pZCAwO1xuICAgICAgcmV0dXJuIHtcbiAgICAgICAgdmFsdWU6IG8gJiYgb1tpKytdLFxuICAgICAgICBkb25lOiAhb1xuICAgICAgfTtcbiAgICB9XG4gIH07XG4gIHRocm93IG5ldyBUeXBlRXJyb3IocyA/IFwiT2JqZWN0IGlzIG5vdCBpdGVyYWJsZS5cIiA6IFwiU3ltYm9sLml0ZXJhdG9yIGlzIG5vdCBkZWZpbmVkLlwiKTtcbn07XG52YXIgX19yZWFkID0gdGhpcyAmJiB0aGlzLl9fcmVhZCB8fCBmdW5jdGlvbiAobywgbikge1xuICB2YXIgbSA9IHR5cGVvZiBTeW1ib2wgPT09IFwiZnVuY3Rpb25cIiAmJiBvW1N5bWJvbC5pdGVyYXRvcl07XG4gIGlmICghbSkgcmV0dXJuIG87XG4gIHZhciBpID0gbS5jYWxsKG8pLFxuICAgIHIsXG4gICAgYXIgPSBbXSxcbiAgICBlO1xuICB0cnkge1xuICAgIHdoaWxlICgobiA9PT0gdm9pZCAwIHx8IG4tLSA+IDApICYmICEociA9IGkubmV4dCgpKS5kb25lKSBhci5wdXNoKHIudmFsdWUpO1xuICB9IGNhdGNoIChlcnJvcikge1xuICAgIGUgPSB7XG4gICAgICBlcnJvcjogZXJyb3JcbiAgICB9O1xuICB9IGZpbmFsbHkge1xuICAgIHRyeSB7XG4gICAgICBpZiAociAmJiAhci5kb25lICYmIChtID0gaVtcInJldHVyblwiXSkpIG0uY2FsbChpKTtcbiAgICB9IGZpbmFsbHkge1xuICAgICAgaWYgKGUpIHRocm93IGUuZXJyb3I7XG4gICAgfVxuICB9XG4gIHJldHVybiBhcjtcbn07XG52YXIgX19zcHJlYWRBcnJheSA9IHRoaXMgJiYgdGhpcy5fX3NwcmVhZEFycmF5IHx8IGZ1bmN0aW9uICh0bywgZnJvbSwgcGFjaykge1xuICBpZiAocGFjayB8fCBhcmd1bWVudHMubGVuZ3RoID09PSAyKSBmb3IgKHZhciBpID0gMCwgbCA9IGZyb20ubGVuZ3RoLCBhcjsgaSA8IGw7IGkrKykge1xuICAgIGlmIChhciB8fCAhKGkgaW4gZnJvbSkpIHtcbiAgICAgIGlmICghYXIpIGFyID0gQXJyYXkucHJvdG90eXBlLnNsaWNlLmNhbGwoZnJvbSwgMCwgaSk7XG4gICAgICBhcltpXSA9IGZyb21baV07XG4gICAgfVxuICB9XG4gIHJldHVybiB0by5jb25jYXQoYXIgfHwgQXJyYXkucHJvdG90eXBlLnNsaWNlLmNhbGwoZnJvbSkpO1xufTtcbnZhciBfX2ltcG9ydERlZmF1bHQgPSB0aGlzICYmIHRoaXMuX19pbXBvcnREZWZhdWx0IHx8IGZ1bmN0aW9uIChtb2QpIHtcbiAgcmV0dXJuIG1vZCAmJiBtb2QuX19lc01vZHVsZSA/IG1vZCA6IHtcbiAgICBcImRlZmF1bHRcIjogbW9kXG4gIH07XG59O1xuT2JqZWN0LmRlZmluZVByb3BlcnR5KGV4cG9ydHMsIFwiX19lc01vZHVsZVwiLCB7XG4gIHZhbHVlOiB0cnVlXG59KTtcbmV4cG9ydHMuUmVxdWlyZUNvbmZpZ3VyYXRpb24gPSBleHBvcnRzLm9wdGlvbnMgPSBleHBvcnRzLlJlcXVpcmVNZXRob2RzID0gZXhwb3J0cy5SZXF1aXJlTG9hZCA9IHZvaWQgMDtcbnZhciBDb25maWd1cmF0aW9uX2pzXzEgPSByZXF1aXJlKFwiLi4vQ29uZmlndXJhdGlvbi5qc1wiKTtcbnZhciBTeW1ib2xNYXBfanNfMSA9IHJlcXVpcmUoXCIuLi9TeW1ib2xNYXAuanNcIik7XG52YXIgVGV4RXJyb3JfanNfMSA9IF9faW1wb3J0RGVmYXVsdChyZXF1aXJlKFwiLi4vVGV4RXJyb3IuanNcIikpO1xudmFyIGdsb2JhbF9qc18xID0gcmVxdWlyZShcIi4uLy4uLy4uL2NvbXBvbmVudHMvZ2xvYmFsLmpzXCIpO1xudmFyIHBhY2thZ2VfanNfMSA9IHJlcXVpcmUoXCIuLi8uLi8uLi9jb21wb25lbnRzL3BhY2thZ2UuanNcIik7XG52YXIgbG9hZGVyX2pzXzEgPSByZXF1aXJlKFwiLi4vLi4vLi4vY29tcG9uZW50cy9sb2FkZXIuanNcIik7XG52YXIgbWF0aGpheF9qc18xID0gcmVxdWlyZShcIi4uLy4uLy4uL21hdGhqYXguanNcIik7XG52YXIgT3B0aW9uc19qc18xID0gcmVxdWlyZShcIi4uLy4uLy4uL3V0aWwvT3B0aW9ucy5qc1wiKTtcbnZhciBNSkNPTkZJRyA9IGdsb2JhbF9qc18xLk1hdGhKYXguY29uZmlnO1xuZnVuY3Rpb24gUmVnaXN0ZXJFeHRlbnNpb24oamF4LCBuYW1lKSB7XG4gIHZhciBfYTtcbiAgdmFyIHJlcXVpcmUgPSBqYXgucGFyc2VPcHRpb25zLm9wdGlvbnMucmVxdWlyZTtcbiAgdmFyIHJlcXVpcmVkID0gamF4LnBhcnNlT3B0aW9ucy5wYWNrYWdlRGF0YS5nZXQoJ3JlcXVpcmUnKS5yZXF1aXJlZDtcbiAgdmFyIGV4dGVuc2lvbiA9IG5hbWUuc3Vic3RyKHJlcXVpcmUucHJlZml4Lmxlbmd0aCk7XG4gIGlmIChyZXF1aXJlZC5pbmRleE9mKGV4dGVuc2lvbikgPCAwKSB7XG4gICAgcmVxdWlyZWQucHVzaChleHRlbnNpb24pO1xuICAgIFJlZ2lzdGVyRGVwZW5kZW5jaWVzKGpheCwgbG9hZGVyX2pzXzEuQ09ORklHLmRlcGVuZGVuY2llc1tuYW1lXSk7XG4gICAgdmFyIGhhbmRsZXIgPSBDb25maWd1cmF0aW9uX2pzXzEuQ29uZmlndXJhdGlvbkhhbmRsZXIuZ2V0KGV4dGVuc2lvbik7XG4gICAgaWYgKGhhbmRsZXIpIHtcbiAgICAgIHZhciBvcHRpb25zXzEgPSBNSkNPTkZJR1tuYW1lXSB8fCB7fTtcbiAgICAgIGlmIChoYW5kbGVyLm9wdGlvbnMgJiYgT2JqZWN0LmtleXMoaGFuZGxlci5vcHRpb25zKS5sZW5ndGggPT09IDEgJiYgaGFuZGxlci5vcHRpb25zW2V4dGVuc2lvbl0pIHtcbiAgICAgICAgb3B0aW9uc18xID0gKF9hID0ge30sIF9hW2V4dGVuc2lvbl0gPSBvcHRpb25zXzEsIF9hKTtcbiAgICAgIH1cbiAgICAgIGpheC5jb25maWd1cmF0aW9uLmFkZChleHRlbnNpb24sIGpheCwgb3B0aW9uc18xKTtcbiAgICAgIHZhciBjb25maWd1cmVkID0gamF4LnBhcnNlT3B0aW9ucy5wYWNrYWdlRGF0YS5nZXQoJ3JlcXVpcmUnKS5jb25maWd1cmVkO1xuICAgICAgaWYgKGhhbmRsZXIucHJlcHJvY2Vzc29ycy5sZW5ndGggJiYgIWNvbmZpZ3VyZWQuaGFzKGV4dGVuc2lvbikpIHtcbiAgICAgICAgY29uZmlndXJlZC5zZXQoZXh0ZW5zaW9uLCB0cnVlKTtcbiAgICAgICAgbWF0aGpheF9qc18xLm1hdGhqYXgucmV0cnlBZnRlcihQcm9taXNlLnJlc29sdmUoKSk7XG4gICAgICB9XG4gICAgfVxuICB9XG59XG5mdW5jdGlvbiBSZWdpc3RlckRlcGVuZGVuY2llcyhqYXgsIG5hbWVzKSB7XG4gIHZhciBlXzEsIF9hO1xuICBpZiAobmFtZXMgPT09IHZvaWQgMCkge1xuICAgIG5hbWVzID0gW107XG4gIH1cbiAgdmFyIHByZWZpeCA9IGpheC5wYXJzZU9wdGlvbnMub3B0aW9ucy5yZXF1aXJlLnByZWZpeDtcbiAgdHJ5IHtcbiAgICBmb3IgKHZhciBuYW1lc18xID0gX192YWx1ZXMobmFtZXMpLCBuYW1lc18xXzEgPSBuYW1lc18xLm5leHQoKTsgIW5hbWVzXzFfMS5kb25lOyBuYW1lc18xXzEgPSBuYW1lc18xLm5leHQoKSkge1xuICAgICAgdmFyIG5hbWVfMSA9IG5hbWVzXzFfMS52YWx1ZTtcbiAgICAgIGlmIChuYW1lXzEuc3Vic3RyKDAsIHByZWZpeC5sZW5ndGgpID09PSBwcmVmaXgpIHtcbiAgICAgICAgUmVnaXN0ZXJFeHRlbnNpb24oamF4LCBuYW1lXzEpO1xuICAgICAgfVxuICAgIH1cbiAgfSBjYXRjaCAoZV8xXzEpIHtcbiAgICBlXzEgPSB7XG4gICAgICBlcnJvcjogZV8xXzFcbiAgICB9O1xuICB9IGZpbmFsbHkge1xuICAgIHRyeSB7XG4gICAgICBpZiAobmFtZXNfMV8xICYmICFuYW1lc18xXzEuZG9uZSAmJiAoX2EgPSBuYW1lc18xLnJldHVybikpIF9hLmNhbGwobmFtZXNfMSk7XG4gICAgfSBmaW5hbGx5IHtcbiAgICAgIGlmIChlXzEpIHRocm93IGVfMS5lcnJvcjtcbiAgICB9XG4gIH1cbn1cbmZ1bmN0aW9uIFJlcXVpcmVMb2FkKHBhcnNlciwgbmFtZSkge1xuICB2YXIgb3B0aW9ucyA9IHBhcnNlci5vcHRpb25zLnJlcXVpcmU7XG4gIHZhciBhbGxvdyA9IG9wdGlvbnMuYWxsb3c7XG4gIHZhciBleHRlbnNpb24gPSAobmFtZS5zdWJzdHIoMCwgMSkgPT09ICdbJyA/ICcnIDogb3B0aW9ucy5wcmVmaXgpICsgbmFtZTtcbiAgdmFyIGFsbG93ZWQgPSBhbGxvdy5oYXNPd25Qcm9wZXJ0eShleHRlbnNpb24pID8gYWxsb3dbZXh0ZW5zaW9uXSA6IGFsbG93Lmhhc093blByb3BlcnR5KG5hbWUpID8gYWxsb3dbbmFtZV0gOiBvcHRpb25zLmRlZmF1bHRBbGxvdztcbiAgaWYgKCFhbGxvd2VkKSB7XG4gICAgdGhyb3cgbmV3IFRleEVycm9yX2pzXzEuZGVmYXVsdCgnQmFkUmVxdWlyZScsICdFeHRlbnNpb24gXCIlMVwiIGlzIG5vdCBhbGxvd2VkIHRvIGJlIGxvYWRlZCcsIGV4dGVuc2lvbik7XG4gIH1cbiAgaWYgKHBhY2thZ2VfanNfMS5QYWNrYWdlLnBhY2thZ2VzLmhhcyhleHRlbnNpb24pKSB7XG4gICAgUmVnaXN0ZXJFeHRlbnNpb24ocGFyc2VyLmNvbmZpZ3VyYXRpb24ucGFja2FnZURhdGEuZ2V0KCdyZXF1aXJlJykuamF4LCBleHRlbnNpb24pO1xuICB9IGVsc2Uge1xuICAgIG1hdGhqYXhfanNfMS5tYXRoamF4LnJldHJ5QWZ0ZXIobG9hZGVyX2pzXzEuTG9hZGVyLmxvYWQoZXh0ZW5zaW9uKSk7XG4gIH1cbn1cbmV4cG9ydHMuUmVxdWlyZUxvYWQgPSBSZXF1aXJlTG9hZDtcbmZ1bmN0aW9uIGNvbmZpZyhfY29uZmlnLCBqYXgpIHtcbiAgamF4LnBhcnNlT3B0aW9ucy5wYWNrYWdlRGF0YS5zZXQoJ3JlcXVpcmUnLCB7XG4gICAgamF4OiBqYXgsXG4gICAgcmVxdWlyZWQ6IF9fc3ByZWFkQXJyYXkoW10sIF9fcmVhZChqYXgub3B0aW9ucy5wYWNrYWdlcyksIGZhbHNlKSxcbiAgICBjb25maWd1cmVkOiBuZXcgTWFwKClcbiAgfSk7XG4gIHZhciBvcHRpb25zID0gamF4LnBhcnNlT3B0aW9ucy5vcHRpb25zLnJlcXVpcmU7XG4gIHZhciBwcmVmaXggPSBvcHRpb25zLnByZWZpeDtcbiAgaWYgKHByZWZpeC5tYXRjaCgvW15fYS16QS1aMC05XS8pKSB7XG4gICAgdGhyb3cgRXJyb3IoJ0lsbGVnYWwgY2hhcmFjdGVycyB1c2VkIGluIFxcXFxyZXF1aXJlIHByZWZpeCcpO1xuICB9XG4gIGlmICghbG9hZGVyX2pzXzEuQ09ORklHLnBhdGhzW3ByZWZpeF0pIHtcbiAgICBsb2FkZXJfanNfMS5DT05GSUcucGF0aHNbcHJlZml4XSA9ICdbbWF0aGpheF0vaW5wdXQvdGV4L2V4dGVuc2lvbnMnO1xuICB9XG4gIG9wdGlvbnMucHJlZml4ID0gJ1snICsgcHJlZml4ICsgJ10vJztcbn1cbmV4cG9ydHMuUmVxdWlyZU1ldGhvZHMgPSB7XG4gIFJlcXVpcmU6IGZ1bmN0aW9uIChwYXJzZXIsIG5hbWUpIHtcbiAgICB2YXIgcmVxdWlyZWQgPSBwYXJzZXIuR2V0QXJndW1lbnQobmFtZSk7XG4gICAgaWYgKHJlcXVpcmVkLm1hdGNoKC9bXl9hLXpBLVowLTldLykgfHwgcmVxdWlyZWQgPT09ICcnKSB7XG4gICAgICB0aHJvdyBuZXcgVGV4RXJyb3JfanNfMS5kZWZhdWx0KCdCYWRQYWNrYWdlTmFtZScsICdBcmd1bWVudCBmb3IgJTEgaXMgbm90IGEgdmFsaWQgcGFja2FnZSBuYW1lJywgbmFtZSk7XG4gICAgfVxuICAgIFJlcXVpcmVMb2FkKHBhcnNlciwgcmVxdWlyZWQpO1xuICB9XG59O1xuZXhwb3J0cy5vcHRpb25zID0ge1xuICByZXF1aXJlOiB7XG4gICAgYWxsb3c6ICgwLCBPcHRpb25zX2pzXzEuZXhwYW5kYWJsZSkoe1xuICAgICAgYmFzZTogZmFsc2UsXG4gICAgICAnYWxsLXBhY2thZ2VzJzogZmFsc2UsXG4gICAgICBhdXRvbG9hZDogZmFsc2UsXG4gICAgICBjb25maWdtYWNyb3M6IGZhbHNlLFxuICAgICAgdGFnZm9ybWF0OiBmYWxzZSxcbiAgICAgIHNldG9wdGlvbnM6IGZhbHNlXG4gICAgfSksXG4gICAgZGVmYXVsdEFsbG93OiB0cnVlLFxuICAgIHByZWZpeDogJ3RleCdcbiAgfVxufTtcbm5ldyBTeW1ib2xNYXBfanNfMS5Db21tYW5kTWFwKCdyZXF1aXJlJywge1xuICByZXF1aXJlOiAnUmVxdWlyZSdcbn0sIGV4cG9ydHMuUmVxdWlyZU1ldGhvZHMpO1xuZXhwb3J0cy5SZXF1aXJlQ29uZmlndXJhdGlvbiA9IENvbmZpZ3VyYXRpb25fanNfMS5Db25maWd1cmF0aW9uLmNyZWF0ZSgncmVxdWlyZScsIHtcbiAgaGFuZGxlcjoge1xuICAgIG1hY3JvOiBbJ3JlcXVpcmUnXVxuICB9LFxuICBjb25maWc6IGNvbmZpZyxcbiAgb3B0aW9uczogZXhwb3J0cy5vcHRpb25zXG59KTsiXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=
"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[1636,3689],{

/***/ 61636:
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
var __assign = this && this.__assign || function () {
  __assign = Object.assign || function (t) {
    for (var s, i = 1, n = arguments.length; i < n; i++) {
      s = arguments[i];
      for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p)) t[p] = s[p];
    }
    return t;
  };
  return __assign.apply(this, arguments);
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
exports.SafeHandler = exports.SafeMathDocumentMixin = void 0;
var safe_js_1 = __webpack_require__(52037);
function SafeMathDocumentMixin(BaseDocument) {
  var _a;
  return _a = function (_super) {
    __extends(class_1, _super);
    function class_1() {
      var e_1, _a;
      var args = [];
      for (var _i = 0; _i < arguments.length; _i++) {
        args[_i] = arguments[_i];
      }
      var _this = _super.apply(this, __spreadArray([], __read(args), false)) || this;
      _this.safe = new _this.options.SafeClass(_this, _this.options.safeOptions);
      var ProcessBits = _this.constructor.ProcessBits;
      if (!ProcessBits.has('safe')) {
        ProcessBits.allocate('safe');
      }
      try {
        for (var _b = __values(_this.inputJax), _c = _b.next(); !_c.done; _c = _b.next()) {
          var jax = _c.value;
          if (jax.name.match(/MathML/)) {
            jax.mathml.filterAttribute = _this.safe.mmlAttribute.bind(_this.safe);
            jax.mathml.filterClassList = _this.safe.mmlClassList.bind(_this.safe);
          } else if (jax.name.match(/TeX/)) {
            jax.postFilters.add(_this.sanitize.bind(jax), -5.5);
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
      return _this;
    }
    class_1.prototype.sanitize = function (data) {
      data.math.root = this.parseOptions.root;
      data.document.safe.sanitize(data.math, data.document);
    };
    return class_1;
  }(BaseDocument), _a.OPTIONS = __assign(__assign({}, BaseDocument.OPTIONS), {
    safeOptions: __assign({}, safe_js_1.Safe.OPTIONS),
    SafeClass: safe_js_1.Safe
  }), _a;
}
exports.SafeMathDocumentMixin = SafeMathDocumentMixin;
function SafeHandler(handler) {
  handler.documentClass = SafeMathDocumentMixin(handler.documentClass);
  return handler;
}
exports.SafeHandler = SafeHandler;

/***/ }),

/***/ 32910:
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
Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports.SafeMethods = void 0;
var lengths_js_1 = __webpack_require__(38655);
exports.SafeMethods = {
  filterURL: function (safe, url) {
    var protocol = (url.match(/^\s*([a-z]+):/i) || [null, ''])[1].toLowerCase();
    var allow = safe.allow.URLs;
    return allow === 'all' || allow === 'safe' && (safe.options.safeProtocols[protocol] || !protocol) ? url : null;
  },
  filterClassList: function (safe, list) {
    var _this = this;
    var classes = list.trim().replace(/\s\s+/g, ' ').split(/ /);
    return classes.map(function (name) {
      return _this.filterClass(safe, name) || '';
    }).join(' ').trim().replace(/\s\s+/g, '');
  },
  filterClass: function (safe, CLASS) {
    var allow = safe.allow.classes;
    return allow === 'all' || allow === 'safe' && CLASS.match(safe.options.classPattern) ? CLASS : null;
  },
  filterID: function (safe, id) {
    var allow = safe.allow.cssIDs;
    return allow === 'all' || allow === 'safe' && id.match(safe.options.idPattern) ? id : null;
  },
  filterStyles: function (safe, styles) {
    var e_1, _a, e_2, _b;
    if (safe.allow.styles === 'all') return styles;
    if (safe.allow.styles !== 'safe') return null;
    var adaptor = safe.adaptor;
    var options = safe.options;
    try {
      var div1 = adaptor.node('div', {
        style: styles
      });
      var div2 = adaptor.node('div');
      try {
        for (var _c = __values(Object.keys(options.safeStyles)), _d = _c.next(); !_d.done; _d = _c.next()) {
          var style = _d.value;
          if (options.styleParts[style]) {
            try {
              for (var _e = (e_2 = void 0, __values(['Top', 'Right', 'Bottom', 'Left'])), _f = _e.next(); !_f.done; _f = _e.next()) {
                var sufix = _f.value;
                var name_1 = style + sufix;
                var value = this.filterStyle(safe, name_1, div1);
                if (value) {
                  adaptor.setStyle(div2, name_1, value);
                }
              }
            } catch (e_2_1) {
              e_2 = {
                error: e_2_1
              };
            } finally {
              try {
                if (_f && !_f.done && (_b = _e.return)) _b.call(_e);
              } finally {
                if (e_2) throw e_2.error;
              }
            }
          } else {
            var value = this.filterStyle(safe, style, div1);
            if (value) {
              adaptor.setStyle(div2, style, value);
            }
          }
        }
      } catch (e_1_1) {
        e_1 = {
          error: e_1_1
        };
      } finally {
        try {
          if (_d && !_d.done && (_a = _c.return)) _a.call(_c);
        } finally {
          if (e_1) throw e_1.error;
        }
      }
      styles = adaptor.allStyles(div2);
    } catch (err) {
      styles = '';
    }
    return styles;
  },
  filterStyle: function (safe, style, div) {
    var value = safe.adaptor.getStyle(div, style);
    if (typeof value !== 'string' || value === '' || value.match(/^\s*calc/) || value.match(/javascript:/) && !safe.options.safeProtocols.javascript || value.match(/data:/) && !safe.options.safeProtocols.data) {
      return null;
    }
    var name = style.replace(/Top|Right|Left|Bottom/, '');
    if (!safe.options.safeStyles[style] && !safe.options.safeStyles[name]) {
      return null;
    }
    return this.filterStyleValue(safe, style, value, div);
  },
  filterStyleValue: function (safe, style, value, div) {
    var name = safe.options.styleLengths[style];
    if (!name) {
      return value;
    }
    if (typeof name !== 'string') {
      return this.filterStyleLength(safe, style, value);
    }
    var length = this.filterStyleLength(safe, name, safe.adaptor.getStyle(div, name));
    if (!length) {
      return null;
    }
    safe.adaptor.setStyle(div, name, length);
    return safe.adaptor.getStyle(div, style);
  },
  filterStyleLength: function (safe, style, value) {
    if (!value.match(/^(.+)(em|ex|ch|rem|px|mm|cm|in|pt|pc|%)$/)) return null;
    var em = (0, lengths_js_1.length2em)(value, 1);
    var lengths = safe.options.styleLengths[style];
    var _a = __read(Array.isArray(lengths) ? lengths : [-safe.options.lengthMax, safe.options.lengthMax], 2),
      m = _a[0],
      M = _a[1];
    return m <= em && em <= M ? value : (em < m ? m : M).toFixed(3).replace(/\.?0+$/, '') + 'em';
  },
  filterFontSize: function (safe, size) {
    return this.filterStyleLength(safe, 'fontSize', size);
  },
  filterSizeMultiplier: function (safe, size) {
    var _a = __read(safe.options.scriptsizemultiplierRange || [-Infinity, Infinity], 2),
      m = _a[0],
      M = _a[1];
    return Math.min(M, Math.max(m, parseFloat(size))).toString();
  },
  filterScriptLevel: function (safe, level) {
    var _a = __read(safe.options.scriptlevelRange || [-Infinity, Infinity], 2),
      m = _a[0],
      M = _a[1];
    return Math.min(M, Math.max(m, parseInt(level))).toString();
  },
  filterData: function (safe, value, id) {
    return id.match(safe.options.dataPattern) ? value : null;
  }
};

/***/ }),

/***/ 52037:
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {



var __assign = this && this.__assign || function () {
  __assign = Object.assign || function (t) {
    for (var s, i = 1, n = arguments.length; i < n; i++) {
      s = arguments[i];
      for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p)) t[p] = s[p];
    }
    return t;
  };
  return __assign.apply(this, arguments);
};
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
exports.Safe = void 0;
var Options_js_1 = __webpack_require__(62704);
var SafeMethods_js_1 = __webpack_require__(32910);
var Safe = function () {
  function Safe(document, options) {
    this.filterAttributes = new Map([['href', 'filterURL'], ['src', 'filterURL'], ['altimg', 'filterURL'], ['class', 'filterClassList'], ['style', 'filterStyles'], ['id', 'filterID'], ['fontsize', 'filterFontSize'], ['mathsize', 'filterFontSize'], ['scriptminsize', 'filterFontSize'], ['scriptsizemultiplier', 'filterSizeMultiplier'], ['scriptlevel', 'filterScriptLevel'], ['data-', 'filterData']]);
    this.filterMethods = __assign({}, SafeMethods_js_1.SafeMethods);
    this.adaptor = document.adaptor;
    this.options = options;
    this.allow = this.options.allow;
  }
  Safe.prototype.sanitize = function (math, document) {
    try {
      math.root.walkTree(this.sanitizeNode.bind(this));
    } catch (err) {
      document.options.compileError(document, math, err);
    }
  };
  Safe.prototype.sanitizeNode = function (node) {
    var e_1, _a;
    var attributes = node.attributes.getAllAttributes();
    try {
      for (var _b = __values(Object.keys(attributes)), _c = _b.next(); !_c.done; _c = _b.next()) {
        var id = _c.value;
        var method = this.filterAttributes.get(id);
        if (method) {
          var value = this.filterMethods[method](this, attributes[id]);
          if (value) {
            if (value !== (typeof value === 'number' ? parseFloat(attributes[id]) : attributes[id])) {
              attributes[id] = value;
            }
          } else {
            delete attributes[id];
          }
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
  Safe.prototype.mmlAttribute = function (id, value) {
    if (id === 'class') return null;
    var method = this.filterAttributes.get(id);
    var filter = method || (id.substr(0, 5) === 'data-' ? this.filterAttributes.get('data-') : null);
    if (!filter) {
      return value;
    }
    var result = this.filterMethods[filter](this, value, id);
    return typeof result === 'number' || typeof result === 'boolean' ? String(result) : result;
  };
  Safe.prototype.mmlClassList = function (list) {
    var _this = this;
    return list.map(function (name) {
      return _this.filterMethods.filterClass(_this, name);
    }).filter(function (value) {
      return value !== null;
    });
  };
  Safe.OPTIONS = {
    allow: {
      URLs: 'safe',
      classes: 'safe',
      cssIDs: 'safe',
      styles: 'safe'
    },
    lengthMax: 3,
    scriptsizemultiplierRange: [.6, 1],
    scriptlevelRange: [-2, 2],
    classPattern: /^mjx-[-a-zA-Z0-9_.]+$/,
    idPattern: /^mjx-[-a-zA-Z0-9_.]+$/,
    dataPattern: /^data-mjx-/,
    safeProtocols: (0, Options_js_1.expandable)({
      http: true,
      https: true,
      file: true,
      javascript: false,
      data: false
    }),
    safeStyles: (0, Options_js_1.expandable)({
      color: true,
      backgroundColor: true,
      border: true,
      cursor: true,
      margin: true,
      padding: true,
      textShadow: true,
      fontFamily: true,
      fontSize: true,
      fontStyle: true,
      fontWeight: true,
      opacity: true,
      outline: true
    }),
    styleParts: (0, Options_js_1.expandable)({
      border: true,
      padding: true,
      margin: true,
      outline: true
    }),
    styleLengths: (0, Options_js_1.expandable)({
      borderTop: 'borderTopWidth',
      borderRight: 'borderRightWidth',
      borderBottom: 'borderBottomWidth',
      borderLeft: 'borderLeftWidth',
      paddingTop: true,
      paddingRight: true,
      paddingBottom: true,
      paddingLeft: true,
      marginTop: true,
      marginRight: true,
      marginBottom: true,
      marginLeft: true,
      outlineTop: true,
      outlineRight: true,
      outlineBottom: true,
      outlineLeft: true,
      fontSize: [.707, 1.44]
    })
  };
  return Safe;
}();
exports.Safe = Safe;

/***/ }),

/***/ 62704:
/***/ (function(__unused_webpack_module, exports) {



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
exports.lookup = exports.separateOptions = exports.selectOptionsFromKeys = exports.selectOptions = exports.userOptions = exports.defaultOptions = exports.insert = exports.copy = exports.keys = exports.makeArray = exports.expandable = exports.Expandable = exports.OPTIONS = exports.REMOVE = exports.APPEND = exports.isObject = void 0;
var OBJECT = {}.constructor;
function isObject(obj) {
  return typeof obj === 'object' && obj !== null && (obj.constructor === OBJECT || obj.constructor === Expandable);
}
exports.isObject = isObject;
exports.APPEND = '[+]';
exports.REMOVE = '[-]';
exports.OPTIONS = {
  invalidOption: 'warn',
  optionError: function (message, _key) {
    if (exports.OPTIONS.invalidOption === 'fatal') {
      throw new Error(message);
    }
    console.warn('MathJax: ' + message);
  }
};
var Expandable = function () {
  function Expandable() {}
  return Expandable;
}();
exports.Expandable = Expandable;
function expandable(def) {
  return Object.assign(Object.create(Expandable.prototype), def);
}
exports.expandable = expandable;
function makeArray(x) {
  return Array.isArray(x) ? x : [x];
}
exports.makeArray = makeArray;
function keys(def) {
  if (!def) {
    return [];
  }
  return Object.keys(def).concat(Object.getOwnPropertySymbols(def));
}
exports.keys = keys;
function copy(def) {
  var e_1, _a;
  var props = {};
  try {
    for (var _b = __values(keys(def)), _c = _b.next(); !_c.done; _c = _b.next()) {
      var key = _c.value;
      var prop = Object.getOwnPropertyDescriptor(def, key);
      var value = prop.value;
      if (Array.isArray(value)) {
        prop.value = insert([], value, false);
      } else if (isObject(value)) {
        prop.value = copy(value);
      }
      if (prop.enumerable) {
        props[key] = prop;
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
  return Object.defineProperties(def.constructor === Expandable ? expandable({}) : {}, props);
}
exports.copy = copy;
function insert(dst, src, warn) {
  var e_2, _a;
  if (warn === void 0) {
    warn = true;
  }
  var _loop_1 = function (key) {
    if (warn && dst[key] === undefined && dst.constructor !== Expandable) {
      if (typeof key === 'symbol') {
        key = key.toString();
      }
      exports.OPTIONS.optionError("Invalid option \"".concat(key, "\" (no default value)."), key);
      return "continue";
    }
    var sval = src[key],
      dval = dst[key];
    if (isObject(sval) && dval !== null && (typeof dval === 'object' || typeof dval === 'function')) {
      var ids = keys(sval);
      if (Array.isArray(dval) && (ids.length === 1 && (ids[0] === exports.APPEND || ids[0] === exports.REMOVE) && Array.isArray(sval[ids[0]]) || ids.length === 2 && ids.sort().join(',') === exports.APPEND + ',' + exports.REMOVE && Array.isArray(sval[exports.APPEND]) && Array.isArray(sval[exports.REMOVE]))) {
        if (sval[exports.REMOVE]) {
          dval = dst[key] = dval.filter(function (x) {
            return sval[exports.REMOVE].indexOf(x) < 0;
          });
        }
        if (sval[exports.APPEND]) {
          dst[key] = __spreadArray(__spreadArray([], __read(dval), false), __read(sval[exports.APPEND]), false);
        }
      } else {
        insert(dval, sval, warn);
      }
    } else if (Array.isArray(sval)) {
      dst[key] = [];
      insert(dst[key], sval, false);
    } else if (isObject(sval)) {
      dst[key] = copy(sval);
    } else {
      dst[key] = sval;
    }
  };
  try {
    for (var _b = __values(keys(src)), _c = _b.next(); !_c.done; _c = _b.next()) {
      var key = _c.value;
      _loop_1(key);
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
exports.insert = insert;
function defaultOptions(options) {
  var defs = [];
  for (var _i = 1; _i < arguments.length; _i++) {
    defs[_i - 1] = arguments[_i];
  }
  defs.forEach(function (def) {
    return insert(options, def, false);
  });
  return options;
}
exports.defaultOptions = defaultOptions;
function userOptions(options) {
  var defs = [];
  for (var _i = 1; _i < arguments.length; _i++) {
    defs[_i - 1] = arguments[_i];
  }
  defs.forEach(function (def) {
    return insert(options, def, true);
  });
  return options;
}
exports.userOptions = userOptions;
function selectOptions(options) {
  var e_3, _a;
  var keys = [];
  for (var _i = 1; _i < arguments.length; _i++) {
    keys[_i - 1] = arguments[_i];
  }
  var subset = {};
  try {
    for (var keys_1 = __values(keys), keys_1_1 = keys_1.next(); !keys_1_1.done; keys_1_1 = keys_1.next()) {
      var key = keys_1_1.value;
      if (options.hasOwnProperty(key)) {
        subset[key] = options[key];
      }
    }
  } catch (e_3_1) {
    e_3 = {
      error: e_3_1
    };
  } finally {
    try {
      if (keys_1_1 && !keys_1_1.done && (_a = keys_1.return)) _a.call(keys_1);
    } finally {
      if (e_3) throw e_3.error;
    }
  }
  return subset;
}
exports.selectOptions = selectOptions;
function selectOptionsFromKeys(options, object) {
  return selectOptions.apply(void 0, __spreadArray([options], __read(Object.keys(object)), false));
}
exports.selectOptionsFromKeys = selectOptionsFromKeys;
function separateOptions(options) {
  var e_4, _a, e_5, _b;
  var objects = [];
  for (var _i = 1; _i < arguments.length; _i++) {
    objects[_i - 1] = arguments[_i];
  }
  var results = [];
  try {
    for (var objects_1 = __values(objects), objects_1_1 = objects_1.next(); !objects_1_1.done; objects_1_1 = objects_1.next()) {
      var object = objects_1_1.value;
      var exists = {},
        missing = {};
      try {
        for (var _c = (e_5 = void 0, __values(Object.keys(options || {}))), _d = _c.next(); !_d.done; _d = _c.next()) {
          var key = _d.value;
          (object[key] === undefined ? missing : exists)[key] = options[key];
        }
      } catch (e_5_1) {
        e_5 = {
          error: e_5_1
        };
      } finally {
        try {
          if (_d && !_d.done && (_b = _c.return)) _b.call(_c);
        } finally {
          if (e_5) throw e_5.error;
        }
      }
      results.push(exists);
      options = missing;
    }
  } catch (e_4_1) {
    e_4 = {
      error: e_4_1
    };
  } finally {
    try {
      if (objects_1_1 && !objects_1_1.done && (_a = objects_1.return)) _a.call(objects_1);
    } finally {
      if (e_4) throw e_4.error;
    }
  }
  results.unshift(options);
  return results;
}
exports.separateOptions = separateOptions;
function lookup(name, lookup, def) {
  if (def === void 0) {
    def = null;
  }
  return lookup.hasOwnProperty(name) ? lookup[name] : def;
}
exports.lookup = lookup;

/***/ }),

/***/ 38655:
/***/ ((__unused_webpack_module, exports) => {



Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports.px = exports.emRounded = exports.em = exports.percent = exports.length2em = exports.MATHSPACE = exports.RELUNITS = exports.UNITS = exports.BIGDIMEN = void 0;
exports.BIGDIMEN = 1000000;
exports.UNITS = {
  px: 1,
  'in': 96,
  cm: 96 / 2.54,
  mm: 96 / 25.4
};
exports.RELUNITS = {
  em: 1,
  ex: .431,
  pt: 1 / 10,
  pc: 12 / 10,
  mu: 1 / 18
};
exports.MATHSPACE = {
  veryverythinmathspace: 1 / 18,
  verythinmathspace: 2 / 18,
  thinmathspace: 3 / 18,
  mediummathspace: 4 / 18,
  thickmathspace: 5 / 18,
  verythickmathspace: 6 / 18,
  veryverythickmathspace: 7 / 18,
  negativeveryverythinmathspace: -1 / 18,
  negativeverythinmathspace: -2 / 18,
  negativethinmathspace: -3 / 18,
  negativemediummathspace: -4 / 18,
  negativethickmathspace: -5 / 18,
  negativeverythickmathspace: -6 / 18,
  negativeveryverythickmathspace: -7 / 18,
  thin: .04,
  medium: .06,
  thick: .1,
  normal: 1,
  big: 2,
  small: 1 / Math.sqrt(2),
  infinity: exports.BIGDIMEN
};
function length2em(length, size, scale, em) {
  if (size === void 0) {
    size = 0;
  }
  if (scale === void 0) {
    scale = 1;
  }
  if (em === void 0) {
    em = 16;
  }
  if (typeof length !== 'string') {
    length = String(length);
  }
  if (length === '' || length == null) {
    return size;
  }
  if (exports.MATHSPACE[length]) {
    return exports.MATHSPACE[length];
  }
  var match = length.match(/^\s*([-+]?(?:\.\d+|\d+(?:\.\d*)?))?(pt|em|ex|mu|px|pc|in|mm|cm|%)?/);
  if (!match) {
    return size;
  }
  var m = parseFloat(match[1] || '1'),
    unit = match[2];
  if (exports.UNITS.hasOwnProperty(unit)) {
    return m * exports.UNITS[unit] / em / scale;
  }
  if (exports.RELUNITS.hasOwnProperty(unit)) {
    return m * exports.RELUNITS[unit];
  }
  if (unit === '%') {
    return m / 100 * size;
  }
  return m * size;
}
exports.length2em = length2em;
function percent(m) {
  return (100 * m).toFixed(1).replace(/\.?0+$/, '') + '%';
}
exports.percent = percent;
function em(m) {
  if (Math.abs(m) < .001) return '0';
  return m.toFixed(3).replace(/\.?0+$/, '') + 'em';
}
exports.em = em;
function emRounded(m, em) {
  if (em === void 0) {
    em = 16;
  }
  m = (Math.round(m * em) + .05) / em;
  if (Math.abs(m) < .001) return '0em';
  return m.toFixed(3).replace(/\.?0+$/, '') + 'em';
}
exports.emRounded = emRounded;
function px(m, M, em) {
  if (M === void 0) {
    M = -exports.BIGDIMEN;
  }
  if (em === void 0) {
    em = 16;
  }
  m *= em;
  if (M && m < M) m = M;
  if (Math.abs(m) < .1) return '0';
  return m.toFixed(1).replace(/\.0$/, '') + 'px';
}
exports.px = px;

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiMTYzNi5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7QUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7Ozs7OztBQzFJQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOzs7Ozs7O0FDbExBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7Ozs7Ozs7QUNoS0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7Ozs7OztBQzNSQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AZGF0YWxheWVyL2p1cHl0ZXItdmlld2VyLy4vbm9kZV9tb2R1bGVzL21hdGhqYXgtZnVsbC9qcy91aS9zYWZlL1NhZmVIYW5kbGVyLmpzIiwid2VicGFjazovL0BkYXRhbGF5ZXIvanVweXRlci12aWV3ZXIvLi9ub2RlX21vZHVsZXMvbWF0aGpheC1mdWxsL2pzL3VpL3NhZmUvU2FmZU1ldGhvZHMuanMiLCJ3ZWJwYWNrOi8vQGRhdGFsYXllci9qdXB5dGVyLXZpZXdlci8uL25vZGVfbW9kdWxlcy9tYXRoamF4LWZ1bGwvanMvdWkvc2FmZS9zYWZlLmpzIiwid2VicGFjazovL0BkYXRhbGF5ZXIvanVweXRlci12aWV3ZXIvLi9ub2RlX21vZHVsZXMvbWF0aGpheC1mdWxsL2pzL3V0aWwvT3B0aW9ucy5qcyIsIndlYnBhY2s6Ly9AZGF0YWxheWVyL2p1cHl0ZXItdmlld2VyLy4vbm9kZV9tb2R1bGVzL21hdGhqYXgtZnVsbC9qcy91dGlsL2xlbmd0aHMuanMiXSwic291cmNlc0NvbnRlbnQiOlsiXCJ1c2Ugc3RyaWN0XCI7XG5cbnZhciBfX2V4dGVuZHMgPSB0aGlzICYmIHRoaXMuX19leHRlbmRzIHx8IGZ1bmN0aW9uICgpIHtcbiAgdmFyIGV4dGVuZFN0YXRpY3MgPSBmdW5jdGlvbiAoZCwgYikge1xuICAgIGV4dGVuZFN0YXRpY3MgPSBPYmplY3Quc2V0UHJvdG90eXBlT2YgfHwge1xuICAgICAgX19wcm90b19fOiBbXVxuICAgIH0gaW5zdGFuY2VvZiBBcnJheSAmJiBmdW5jdGlvbiAoZCwgYikge1xuICAgICAgZC5fX3Byb3RvX18gPSBiO1xuICAgIH0gfHwgZnVuY3Rpb24gKGQsIGIpIHtcbiAgICAgIGZvciAodmFyIHAgaW4gYikgaWYgKE9iamVjdC5wcm90b3R5cGUuaGFzT3duUHJvcGVydHkuY2FsbChiLCBwKSkgZFtwXSA9IGJbcF07XG4gICAgfTtcbiAgICByZXR1cm4gZXh0ZW5kU3RhdGljcyhkLCBiKTtcbiAgfTtcbiAgcmV0dXJuIGZ1bmN0aW9uIChkLCBiKSB7XG4gICAgaWYgKHR5cGVvZiBiICE9PSBcImZ1bmN0aW9uXCIgJiYgYiAhPT0gbnVsbCkgdGhyb3cgbmV3IFR5cGVFcnJvcihcIkNsYXNzIGV4dGVuZHMgdmFsdWUgXCIgKyBTdHJpbmcoYikgKyBcIiBpcyBub3QgYSBjb25zdHJ1Y3RvciBvciBudWxsXCIpO1xuICAgIGV4dGVuZFN0YXRpY3MoZCwgYik7XG4gICAgZnVuY3Rpb24gX18oKSB7XG4gICAgICB0aGlzLmNvbnN0cnVjdG9yID0gZDtcbiAgICB9XG4gICAgZC5wcm90b3R5cGUgPSBiID09PSBudWxsID8gT2JqZWN0LmNyZWF0ZShiKSA6IChfXy5wcm90b3R5cGUgPSBiLnByb3RvdHlwZSwgbmV3IF9fKCkpO1xuICB9O1xufSgpO1xudmFyIF9fYXNzaWduID0gdGhpcyAmJiB0aGlzLl9fYXNzaWduIHx8IGZ1bmN0aW9uICgpIHtcbiAgX19hc3NpZ24gPSBPYmplY3QuYXNzaWduIHx8IGZ1bmN0aW9uICh0KSB7XG4gICAgZm9yICh2YXIgcywgaSA9IDEsIG4gPSBhcmd1bWVudHMubGVuZ3RoOyBpIDwgbjsgaSsrKSB7XG4gICAgICBzID0gYXJndW1lbnRzW2ldO1xuICAgICAgZm9yICh2YXIgcCBpbiBzKSBpZiAoT2JqZWN0LnByb3RvdHlwZS5oYXNPd25Qcm9wZXJ0eS5jYWxsKHMsIHApKSB0W3BdID0gc1twXTtcbiAgICB9XG4gICAgcmV0dXJuIHQ7XG4gIH07XG4gIHJldHVybiBfX2Fzc2lnbi5hcHBseSh0aGlzLCBhcmd1bWVudHMpO1xufTtcbnZhciBfX3JlYWQgPSB0aGlzICYmIHRoaXMuX19yZWFkIHx8IGZ1bmN0aW9uIChvLCBuKSB7XG4gIHZhciBtID0gdHlwZW9mIFN5bWJvbCA9PT0gXCJmdW5jdGlvblwiICYmIG9bU3ltYm9sLml0ZXJhdG9yXTtcbiAgaWYgKCFtKSByZXR1cm4gbztcbiAgdmFyIGkgPSBtLmNhbGwobyksXG4gICAgcixcbiAgICBhciA9IFtdLFxuICAgIGU7XG4gIHRyeSB7XG4gICAgd2hpbGUgKChuID09PSB2b2lkIDAgfHwgbi0tID4gMCkgJiYgIShyID0gaS5uZXh0KCkpLmRvbmUpIGFyLnB1c2goci52YWx1ZSk7XG4gIH0gY2F0Y2ggKGVycm9yKSB7XG4gICAgZSA9IHtcbiAgICAgIGVycm9yOiBlcnJvclxuICAgIH07XG4gIH0gZmluYWxseSB7XG4gICAgdHJ5IHtcbiAgICAgIGlmIChyICYmICFyLmRvbmUgJiYgKG0gPSBpW1wicmV0dXJuXCJdKSkgbS5jYWxsKGkpO1xuICAgIH0gZmluYWxseSB7XG4gICAgICBpZiAoZSkgdGhyb3cgZS5lcnJvcjtcbiAgICB9XG4gIH1cbiAgcmV0dXJuIGFyO1xufTtcbnZhciBfX3NwcmVhZEFycmF5ID0gdGhpcyAmJiB0aGlzLl9fc3ByZWFkQXJyYXkgfHwgZnVuY3Rpb24gKHRvLCBmcm9tLCBwYWNrKSB7XG4gIGlmIChwYWNrIHx8IGFyZ3VtZW50cy5sZW5ndGggPT09IDIpIGZvciAodmFyIGkgPSAwLCBsID0gZnJvbS5sZW5ndGgsIGFyOyBpIDwgbDsgaSsrKSB7XG4gICAgaWYgKGFyIHx8ICEoaSBpbiBmcm9tKSkge1xuICAgICAgaWYgKCFhcikgYXIgPSBBcnJheS5wcm90b3R5cGUuc2xpY2UuY2FsbChmcm9tLCAwLCBpKTtcbiAgICAgIGFyW2ldID0gZnJvbVtpXTtcbiAgICB9XG4gIH1cbiAgcmV0dXJuIHRvLmNvbmNhdChhciB8fCBBcnJheS5wcm90b3R5cGUuc2xpY2UuY2FsbChmcm9tKSk7XG59O1xudmFyIF9fdmFsdWVzID0gdGhpcyAmJiB0aGlzLl9fdmFsdWVzIHx8IGZ1bmN0aW9uIChvKSB7XG4gIHZhciBzID0gdHlwZW9mIFN5bWJvbCA9PT0gXCJmdW5jdGlvblwiICYmIFN5bWJvbC5pdGVyYXRvcixcbiAgICBtID0gcyAmJiBvW3NdLFxuICAgIGkgPSAwO1xuICBpZiAobSkgcmV0dXJuIG0uY2FsbChvKTtcbiAgaWYgKG8gJiYgdHlwZW9mIG8ubGVuZ3RoID09PSBcIm51bWJlclwiKSByZXR1cm4ge1xuICAgIG5leHQ6IGZ1bmN0aW9uICgpIHtcbiAgICAgIGlmIChvICYmIGkgPj0gby5sZW5ndGgpIG8gPSB2b2lkIDA7XG4gICAgICByZXR1cm4ge1xuICAgICAgICB2YWx1ZTogbyAmJiBvW2krK10sXG4gICAgICAgIGRvbmU6ICFvXG4gICAgICB9O1xuICAgIH1cbiAgfTtcbiAgdGhyb3cgbmV3IFR5cGVFcnJvcihzID8gXCJPYmplY3QgaXMgbm90IGl0ZXJhYmxlLlwiIDogXCJTeW1ib2wuaXRlcmF0b3IgaXMgbm90IGRlZmluZWQuXCIpO1xufTtcbk9iamVjdC5kZWZpbmVQcm9wZXJ0eShleHBvcnRzLCBcIl9fZXNNb2R1bGVcIiwge1xuICB2YWx1ZTogdHJ1ZVxufSk7XG5leHBvcnRzLlNhZmVIYW5kbGVyID0gZXhwb3J0cy5TYWZlTWF0aERvY3VtZW50TWl4aW4gPSB2b2lkIDA7XG52YXIgc2FmZV9qc18xID0gcmVxdWlyZShcIi4vc2FmZS5qc1wiKTtcbmZ1bmN0aW9uIFNhZmVNYXRoRG9jdW1lbnRNaXhpbihCYXNlRG9jdW1lbnQpIHtcbiAgdmFyIF9hO1xuICByZXR1cm4gX2EgPSBmdW5jdGlvbiAoX3N1cGVyKSB7XG4gICAgX19leHRlbmRzKGNsYXNzXzEsIF9zdXBlcik7XG4gICAgZnVuY3Rpb24gY2xhc3NfMSgpIHtcbiAgICAgIHZhciBlXzEsIF9hO1xuICAgICAgdmFyIGFyZ3MgPSBbXTtcbiAgICAgIGZvciAodmFyIF9pID0gMDsgX2kgPCBhcmd1bWVudHMubGVuZ3RoOyBfaSsrKSB7XG4gICAgICAgIGFyZ3NbX2ldID0gYXJndW1lbnRzW19pXTtcbiAgICAgIH1cbiAgICAgIHZhciBfdGhpcyA9IF9zdXBlci5hcHBseSh0aGlzLCBfX3NwcmVhZEFycmF5KFtdLCBfX3JlYWQoYXJncyksIGZhbHNlKSkgfHwgdGhpcztcbiAgICAgIF90aGlzLnNhZmUgPSBuZXcgX3RoaXMub3B0aW9ucy5TYWZlQ2xhc3MoX3RoaXMsIF90aGlzLm9wdGlvbnMuc2FmZU9wdGlvbnMpO1xuICAgICAgdmFyIFByb2Nlc3NCaXRzID0gX3RoaXMuY29uc3RydWN0b3IuUHJvY2Vzc0JpdHM7XG4gICAgICBpZiAoIVByb2Nlc3NCaXRzLmhhcygnc2FmZScpKSB7XG4gICAgICAgIFByb2Nlc3NCaXRzLmFsbG9jYXRlKCdzYWZlJyk7XG4gICAgICB9XG4gICAgICB0cnkge1xuICAgICAgICBmb3IgKHZhciBfYiA9IF9fdmFsdWVzKF90aGlzLmlucHV0SmF4KSwgX2MgPSBfYi5uZXh0KCk7ICFfYy5kb25lOyBfYyA9IF9iLm5leHQoKSkge1xuICAgICAgICAgIHZhciBqYXggPSBfYy52YWx1ZTtcbiAgICAgICAgICBpZiAoamF4Lm5hbWUubWF0Y2goL01hdGhNTC8pKSB7XG4gICAgICAgICAgICBqYXgubWF0aG1sLmZpbHRlckF0dHJpYnV0ZSA9IF90aGlzLnNhZmUubW1sQXR0cmlidXRlLmJpbmQoX3RoaXMuc2FmZSk7XG4gICAgICAgICAgICBqYXgubWF0aG1sLmZpbHRlckNsYXNzTGlzdCA9IF90aGlzLnNhZmUubW1sQ2xhc3NMaXN0LmJpbmQoX3RoaXMuc2FmZSk7XG4gICAgICAgICAgfSBlbHNlIGlmIChqYXgubmFtZS5tYXRjaCgvVGVYLykpIHtcbiAgICAgICAgICAgIGpheC5wb3N0RmlsdGVycy5hZGQoX3RoaXMuc2FuaXRpemUuYmluZChqYXgpLCAtNS41KTtcbiAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICAgIH0gY2F0Y2ggKGVfMV8xKSB7XG4gICAgICAgIGVfMSA9IHtcbiAgICAgICAgICBlcnJvcjogZV8xXzFcbiAgICAgICAgfTtcbiAgICAgIH0gZmluYWxseSB7XG4gICAgICAgIHRyeSB7XG4gICAgICAgICAgaWYgKF9jICYmICFfYy5kb25lICYmIChfYSA9IF9iLnJldHVybikpIF9hLmNhbGwoX2IpO1xuICAgICAgICB9IGZpbmFsbHkge1xuICAgICAgICAgIGlmIChlXzEpIHRocm93IGVfMS5lcnJvcjtcbiAgICAgICAgfVxuICAgICAgfVxuICAgICAgcmV0dXJuIF90aGlzO1xuICAgIH1cbiAgICBjbGFzc18xLnByb3RvdHlwZS5zYW5pdGl6ZSA9IGZ1bmN0aW9uIChkYXRhKSB7XG4gICAgICBkYXRhLm1hdGgucm9vdCA9IHRoaXMucGFyc2VPcHRpb25zLnJvb3Q7XG4gICAgICBkYXRhLmRvY3VtZW50LnNhZmUuc2FuaXRpemUoZGF0YS5tYXRoLCBkYXRhLmRvY3VtZW50KTtcbiAgICB9O1xuICAgIHJldHVybiBjbGFzc18xO1xuICB9KEJhc2VEb2N1bWVudCksIF9hLk9QVElPTlMgPSBfX2Fzc2lnbihfX2Fzc2lnbih7fSwgQmFzZURvY3VtZW50Lk9QVElPTlMpLCB7XG4gICAgc2FmZU9wdGlvbnM6IF9fYXNzaWduKHt9LCBzYWZlX2pzXzEuU2FmZS5PUFRJT05TKSxcbiAgICBTYWZlQ2xhc3M6IHNhZmVfanNfMS5TYWZlXG4gIH0pLCBfYTtcbn1cbmV4cG9ydHMuU2FmZU1hdGhEb2N1bWVudE1peGluID0gU2FmZU1hdGhEb2N1bWVudE1peGluO1xuZnVuY3Rpb24gU2FmZUhhbmRsZXIoaGFuZGxlcikge1xuICBoYW5kbGVyLmRvY3VtZW50Q2xhc3MgPSBTYWZlTWF0aERvY3VtZW50TWl4aW4oaGFuZGxlci5kb2N1bWVudENsYXNzKTtcbiAgcmV0dXJuIGhhbmRsZXI7XG59XG5leHBvcnRzLlNhZmVIYW5kbGVyID0gU2FmZUhhbmRsZXI7IiwiXCJ1c2Ugc3RyaWN0XCI7XG5cbnZhciBfX3ZhbHVlcyA9IHRoaXMgJiYgdGhpcy5fX3ZhbHVlcyB8fCBmdW5jdGlvbiAobykge1xuICB2YXIgcyA9IHR5cGVvZiBTeW1ib2wgPT09IFwiZnVuY3Rpb25cIiAmJiBTeW1ib2wuaXRlcmF0b3IsXG4gICAgbSA9IHMgJiYgb1tzXSxcbiAgICBpID0gMDtcbiAgaWYgKG0pIHJldHVybiBtLmNhbGwobyk7XG4gIGlmIChvICYmIHR5cGVvZiBvLmxlbmd0aCA9PT0gXCJudW1iZXJcIikgcmV0dXJuIHtcbiAgICBuZXh0OiBmdW5jdGlvbiAoKSB7XG4gICAgICBpZiAobyAmJiBpID49IG8ubGVuZ3RoKSBvID0gdm9pZCAwO1xuICAgICAgcmV0dXJuIHtcbiAgICAgICAgdmFsdWU6IG8gJiYgb1tpKytdLFxuICAgICAgICBkb25lOiAhb1xuICAgICAgfTtcbiAgICB9XG4gIH07XG4gIHRocm93IG5ldyBUeXBlRXJyb3IocyA/IFwiT2JqZWN0IGlzIG5vdCBpdGVyYWJsZS5cIiA6IFwiU3ltYm9sLml0ZXJhdG9yIGlzIG5vdCBkZWZpbmVkLlwiKTtcbn07XG52YXIgX19yZWFkID0gdGhpcyAmJiB0aGlzLl9fcmVhZCB8fCBmdW5jdGlvbiAobywgbikge1xuICB2YXIgbSA9IHR5cGVvZiBTeW1ib2wgPT09IFwiZnVuY3Rpb25cIiAmJiBvW1N5bWJvbC5pdGVyYXRvcl07XG4gIGlmICghbSkgcmV0dXJuIG87XG4gIHZhciBpID0gbS5jYWxsKG8pLFxuICAgIHIsXG4gICAgYXIgPSBbXSxcbiAgICBlO1xuICB0cnkge1xuICAgIHdoaWxlICgobiA9PT0gdm9pZCAwIHx8IG4tLSA+IDApICYmICEociA9IGkubmV4dCgpKS5kb25lKSBhci5wdXNoKHIudmFsdWUpO1xuICB9IGNhdGNoIChlcnJvcikge1xuICAgIGUgPSB7XG4gICAgICBlcnJvcjogZXJyb3JcbiAgICB9O1xuICB9IGZpbmFsbHkge1xuICAgIHRyeSB7XG4gICAgICBpZiAociAmJiAhci5kb25lICYmIChtID0gaVtcInJldHVyblwiXSkpIG0uY2FsbChpKTtcbiAgICB9IGZpbmFsbHkge1xuICAgICAgaWYgKGUpIHRocm93IGUuZXJyb3I7XG4gICAgfVxuICB9XG4gIHJldHVybiBhcjtcbn07XG5PYmplY3QuZGVmaW5lUHJvcGVydHkoZXhwb3J0cywgXCJfX2VzTW9kdWxlXCIsIHtcbiAgdmFsdWU6IHRydWVcbn0pO1xuZXhwb3J0cy5TYWZlTWV0aG9kcyA9IHZvaWQgMDtcbnZhciBsZW5ndGhzX2pzXzEgPSByZXF1aXJlKFwiLi4vLi4vdXRpbC9sZW5ndGhzLmpzXCIpO1xuZXhwb3J0cy5TYWZlTWV0aG9kcyA9IHtcbiAgZmlsdGVyVVJMOiBmdW5jdGlvbiAoc2FmZSwgdXJsKSB7XG4gICAgdmFyIHByb3RvY29sID0gKHVybC5tYXRjaCgvXlxccyooW2Etel0rKTovaSkgfHwgW251bGwsICcnXSlbMV0udG9Mb3dlckNhc2UoKTtcbiAgICB2YXIgYWxsb3cgPSBzYWZlLmFsbG93LlVSTHM7XG4gICAgcmV0dXJuIGFsbG93ID09PSAnYWxsJyB8fCBhbGxvdyA9PT0gJ3NhZmUnICYmIChzYWZlLm9wdGlvbnMuc2FmZVByb3RvY29sc1twcm90b2NvbF0gfHwgIXByb3RvY29sKSA/IHVybCA6IG51bGw7XG4gIH0sXG4gIGZpbHRlckNsYXNzTGlzdDogZnVuY3Rpb24gKHNhZmUsIGxpc3QpIHtcbiAgICB2YXIgX3RoaXMgPSB0aGlzO1xuICAgIHZhciBjbGFzc2VzID0gbGlzdC50cmltKCkucmVwbGFjZSgvXFxzXFxzKy9nLCAnICcpLnNwbGl0KC8gLyk7XG4gICAgcmV0dXJuIGNsYXNzZXMubWFwKGZ1bmN0aW9uIChuYW1lKSB7XG4gICAgICByZXR1cm4gX3RoaXMuZmlsdGVyQ2xhc3Moc2FmZSwgbmFtZSkgfHwgJyc7XG4gICAgfSkuam9pbignICcpLnRyaW0oKS5yZXBsYWNlKC9cXHNcXHMrL2csICcnKTtcbiAgfSxcbiAgZmlsdGVyQ2xhc3M6IGZ1bmN0aW9uIChzYWZlLCBDTEFTUykge1xuICAgIHZhciBhbGxvdyA9IHNhZmUuYWxsb3cuY2xhc3NlcztcbiAgICByZXR1cm4gYWxsb3cgPT09ICdhbGwnIHx8IGFsbG93ID09PSAnc2FmZScgJiYgQ0xBU1MubWF0Y2goc2FmZS5vcHRpb25zLmNsYXNzUGF0dGVybikgPyBDTEFTUyA6IG51bGw7XG4gIH0sXG4gIGZpbHRlcklEOiBmdW5jdGlvbiAoc2FmZSwgaWQpIHtcbiAgICB2YXIgYWxsb3cgPSBzYWZlLmFsbG93LmNzc0lEcztcbiAgICByZXR1cm4gYWxsb3cgPT09ICdhbGwnIHx8IGFsbG93ID09PSAnc2FmZScgJiYgaWQubWF0Y2goc2FmZS5vcHRpb25zLmlkUGF0dGVybikgPyBpZCA6IG51bGw7XG4gIH0sXG4gIGZpbHRlclN0eWxlczogZnVuY3Rpb24gKHNhZmUsIHN0eWxlcykge1xuICAgIHZhciBlXzEsIF9hLCBlXzIsIF9iO1xuICAgIGlmIChzYWZlLmFsbG93LnN0eWxlcyA9PT0gJ2FsbCcpIHJldHVybiBzdHlsZXM7XG4gICAgaWYgKHNhZmUuYWxsb3cuc3R5bGVzICE9PSAnc2FmZScpIHJldHVybiBudWxsO1xuICAgIHZhciBhZGFwdG9yID0gc2FmZS5hZGFwdG9yO1xuICAgIHZhciBvcHRpb25zID0gc2FmZS5vcHRpb25zO1xuICAgIHRyeSB7XG4gICAgICB2YXIgZGl2MSA9IGFkYXB0b3Iubm9kZSgnZGl2Jywge1xuICAgICAgICBzdHlsZTogc3R5bGVzXG4gICAgICB9KTtcbiAgICAgIHZhciBkaXYyID0gYWRhcHRvci5ub2RlKCdkaXYnKTtcbiAgICAgIHRyeSB7XG4gICAgICAgIGZvciAodmFyIF9jID0gX192YWx1ZXMoT2JqZWN0LmtleXMob3B0aW9ucy5zYWZlU3R5bGVzKSksIF9kID0gX2MubmV4dCgpOyAhX2QuZG9uZTsgX2QgPSBfYy5uZXh0KCkpIHtcbiAgICAgICAgICB2YXIgc3R5bGUgPSBfZC52YWx1ZTtcbiAgICAgICAgICBpZiAob3B0aW9ucy5zdHlsZVBhcnRzW3N0eWxlXSkge1xuICAgICAgICAgICAgdHJ5IHtcbiAgICAgICAgICAgICAgZm9yICh2YXIgX2UgPSAoZV8yID0gdm9pZCAwLCBfX3ZhbHVlcyhbJ1RvcCcsICdSaWdodCcsICdCb3R0b20nLCAnTGVmdCddKSksIF9mID0gX2UubmV4dCgpOyAhX2YuZG9uZTsgX2YgPSBfZS5uZXh0KCkpIHtcbiAgICAgICAgICAgICAgICB2YXIgc3VmaXggPSBfZi52YWx1ZTtcbiAgICAgICAgICAgICAgICB2YXIgbmFtZV8xID0gc3R5bGUgKyBzdWZpeDtcbiAgICAgICAgICAgICAgICB2YXIgdmFsdWUgPSB0aGlzLmZpbHRlclN0eWxlKHNhZmUsIG5hbWVfMSwgZGl2MSk7XG4gICAgICAgICAgICAgICAgaWYgKHZhbHVlKSB7XG4gICAgICAgICAgICAgICAgICBhZGFwdG9yLnNldFN0eWxlKGRpdjIsIG5hbWVfMSwgdmFsdWUpO1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgfSBjYXRjaCAoZV8yXzEpIHtcbiAgICAgICAgICAgICAgZV8yID0ge1xuICAgICAgICAgICAgICAgIGVycm9yOiBlXzJfMVxuICAgICAgICAgICAgICB9O1xuICAgICAgICAgICAgfSBmaW5hbGx5IHtcbiAgICAgICAgICAgICAgdHJ5IHtcbiAgICAgICAgICAgICAgICBpZiAoX2YgJiYgIV9mLmRvbmUgJiYgKF9iID0gX2UucmV0dXJuKSkgX2IuY2FsbChfZSk7XG4gICAgICAgICAgICAgIH0gZmluYWxseSB7XG4gICAgICAgICAgICAgICAgaWYgKGVfMikgdGhyb3cgZV8yLmVycm9yO1xuICAgICAgICAgICAgICB9XG4gICAgICAgICAgICB9XG4gICAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgIHZhciB2YWx1ZSA9IHRoaXMuZmlsdGVyU3R5bGUoc2FmZSwgc3R5bGUsIGRpdjEpO1xuICAgICAgICAgICAgaWYgKHZhbHVlKSB7XG4gICAgICAgICAgICAgIGFkYXB0b3Iuc2V0U3R5bGUoZGl2Miwgc3R5bGUsIHZhbHVlKTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICAgIH0gY2F0Y2ggKGVfMV8xKSB7XG4gICAgICAgIGVfMSA9IHtcbiAgICAgICAgICBlcnJvcjogZV8xXzFcbiAgICAgICAgfTtcbiAgICAgIH0gZmluYWxseSB7XG4gICAgICAgIHRyeSB7XG4gICAgICAgICAgaWYgKF9kICYmICFfZC5kb25lICYmIChfYSA9IF9jLnJldHVybikpIF9hLmNhbGwoX2MpO1xuICAgICAgICB9IGZpbmFsbHkge1xuICAgICAgICAgIGlmIChlXzEpIHRocm93IGVfMS5lcnJvcjtcbiAgICAgICAgfVxuICAgICAgfVxuICAgICAgc3R5bGVzID0gYWRhcHRvci5hbGxTdHlsZXMoZGl2Mik7XG4gICAgfSBjYXRjaCAoZXJyKSB7XG4gICAgICBzdHlsZXMgPSAnJztcbiAgICB9XG4gICAgcmV0dXJuIHN0eWxlcztcbiAgfSxcbiAgZmlsdGVyU3R5bGU6IGZ1bmN0aW9uIChzYWZlLCBzdHlsZSwgZGl2KSB7XG4gICAgdmFyIHZhbHVlID0gc2FmZS5hZGFwdG9yLmdldFN0eWxlKGRpdiwgc3R5bGUpO1xuICAgIGlmICh0eXBlb2YgdmFsdWUgIT09ICdzdHJpbmcnIHx8IHZhbHVlID09PSAnJyB8fCB2YWx1ZS5tYXRjaCgvXlxccypjYWxjLykgfHwgdmFsdWUubWF0Y2goL2phdmFzY3JpcHQ6LykgJiYgIXNhZmUub3B0aW9ucy5zYWZlUHJvdG9jb2xzLmphdmFzY3JpcHQgfHwgdmFsdWUubWF0Y2goL2RhdGE6LykgJiYgIXNhZmUub3B0aW9ucy5zYWZlUHJvdG9jb2xzLmRhdGEpIHtcbiAgICAgIHJldHVybiBudWxsO1xuICAgIH1cbiAgICB2YXIgbmFtZSA9IHN0eWxlLnJlcGxhY2UoL1RvcHxSaWdodHxMZWZ0fEJvdHRvbS8sICcnKTtcbiAgICBpZiAoIXNhZmUub3B0aW9ucy5zYWZlU3R5bGVzW3N0eWxlXSAmJiAhc2FmZS5vcHRpb25zLnNhZmVTdHlsZXNbbmFtZV0pIHtcbiAgICAgIHJldHVybiBudWxsO1xuICAgIH1cbiAgICByZXR1cm4gdGhpcy5maWx0ZXJTdHlsZVZhbHVlKHNhZmUsIHN0eWxlLCB2YWx1ZSwgZGl2KTtcbiAgfSxcbiAgZmlsdGVyU3R5bGVWYWx1ZTogZnVuY3Rpb24gKHNhZmUsIHN0eWxlLCB2YWx1ZSwgZGl2KSB7XG4gICAgdmFyIG5hbWUgPSBzYWZlLm9wdGlvbnMuc3R5bGVMZW5ndGhzW3N0eWxlXTtcbiAgICBpZiAoIW5hbWUpIHtcbiAgICAgIHJldHVybiB2YWx1ZTtcbiAgICB9XG4gICAgaWYgKHR5cGVvZiBuYW1lICE9PSAnc3RyaW5nJykge1xuICAgICAgcmV0dXJuIHRoaXMuZmlsdGVyU3R5bGVMZW5ndGgoc2FmZSwgc3R5bGUsIHZhbHVlKTtcbiAgICB9XG4gICAgdmFyIGxlbmd0aCA9IHRoaXMuZmlsdGVyU3R5bGVMZW5ndGgoc2FmZSwgbmFtZSwgc2FmZS5hZGFwdG9yLmdldFN0eWxlKGRpdiwgbmFtZSkpO1xuICAgIGlmICghbGVuZ3RoKSB7XG4gICAgICByZXR1cm4gbnVsbDtcbiAgICB9XG4gICAgc2FmZS5hZGFwdG9yLnNldFN0eWxlKGRpdiwgbmFtZSwgbGVuZ3RoKTtcbiAgICByZXR1cm4gc2FmZS5hZGFwdG9yLmdldFN0eWxlKGRpdiwgc3R5bGUpO1xuICB9LFxuICBmaWx0ZXJTdHlsZUxlbmd0aDogZnVuY3Rpb24gKHNhZmUsIHN0eWxlLCB2YWx1ZSkge1xuICAgIGlmICghdmFsdWUubWF0Y2goL14oLispKGVtfGV4fGNofHJlbXxweHxtbXxjbXxpbnxwdHxwY3wlKSQvKSkgcmV0dXJuIG51bGw7XG4gICAgdmFyIGVtID0gKDAsIGxlbmd0aHNfanNfMS5sZW5ndGgyZW0pKHZhbHVlLCAxKTtcbiAgICB2YXIgbGVuZ3RocyA9IHNhZmUub3B0aW9ucy5zdHlsZUxlbmd0aHNbc3R5bGVdO1xuICAgIHZhciBfYSA9IF9fcmVhZChBcnJheS5pc0FycmF5KGxlbmd0aHMpID8gbGVuZ3RocyA6IFstc2FmZS5vcHRpb25zLmxlbmd0aE1heCwgc2FmZS5vcHRpb25zLmxlbmd0aE1heF0sIDIpLFxuICAgICAgbSA9IF9hWzBdLFxuICAgICAgTSA9IF9hWzFdO1xuICAgIHJldHVybiBtIDw9IGVtICYmIGVtIDw9IE0gPyB2YWx1ZSA6IChlbSA8IG0gPyBtIDogTSkudG9GaXhlZCgzKS5yZXBsYWNlKC9cXC4/MCskLywgJycpICsgJ2VtJztcbiAgfSxcbiAgZmlsdGVyRm9udFNpemU6IGZ1bmN0aW9uIChzYWZlLCBzaXplKSB7XG4gICAgcmV0dXJuIHRoaXMuZmlsdGVyU3R5bGVMZW5ndGgoc2FmZSwgJ2ZvbnRTaXplJywgc2l6ZSk7XG4gIH0sXG4gIGZpbHRlclNpemVNdWx0aXBsaWVyOiBmdW5jdGlvbiAoc2FmZSwgc2l6ZSkge1xuICAgIHZhciBfYSA9IF9fcmVhZChzYWZlLm9wdGlvbnMuc2NyaXB0c2l6ZW11bHRpcGxpZXJSYW5nZSB8fCBbLUluZmluaXR5LCBJbmZpbml0eV0sIDIpLFxuICAgICAgbSA9IF9hWzBdLFxuICAgICAgTSA9IF9hWzFdO1xuICAgIHJldHVybiBNYXRoLm1pbihNLCBNYXRoLm1heChtLCBwYXJzZUZsb2F0KHNpemUpKSkudG9TdHJpbmcoKTtcbiAgfSxcbiAgZmlsdGVyU2NyaXB0TGV2ZWw6IGZ1bmN0aW9uIChzYWZlLCBsZXZlbCkge1xuICAgIHZhciBfYSA9IF9fcmVhZChzYWZlLm9wdGlvbnMuc2NyaXB0bGV2ZWxSYW5nZSB8fCBbLUluZmluaXR5LCBJbmZpbml0eV0sIDIpLFxuICAgICAgbSA9IF9hWzBdLFxuICAgICAgTSA9IF9hWzFdO1xuICAgIHJldHVybiBNYXRoLm1pbihNLCBNYXRoLm1heChtLCBwYXJzZUludChsZXZlbCkpKS50b1N0cmluZygpO1xuICB9LFxuICBmaWx0ZXJEYXRhOiBmdW5jdGlvbiAoc2FmZSwgdmFsdWUsIGlkKSB7XG4gICAgcmV0dXJuIGlkLm1hdGNoKHNhZmUub3B0aW9ucy5kYXRhUGF0dGVybikgPyB2YWx1ZSA6IG51bGw7XG4gIH1cbn07IiwiXCJ1c2Ugc3RyaWN0XCI7XG5cbnZhciBfX2Fzc2lnbiA9IHRoaXMgJiYgdGhpcy5fX2Fzc2lnbiB8fCBmdW5jdGlvbiAoKSB7XG4gIF9fYXNzaWduID0gT2JqZWN0LmFzc2lnbiB8fCBmdW5jdGlvbiAodCkge1xuICAgIGZvciAodmFyIHMsIGkgPSAxLCBuID0gYXJndW1lbnRzLmxlbmd0aDsgaSA8IG47IGkrKykge1xuICAgICAgcyA9IGFyZ3VtZW50c1tpXTtcbiAgICAgIGZvciAodmFyIHAgaW4gcykgaWYgKE9iamVjdC5wcm90b3R5cGUuaGFzT3duUHJvcGVydHkuY2FsbChzLCBwKSkgdFtwXSA9IHNbcF07XG4gICAgfVxuICAgIHJldHVybiB0O1xuICB9O1xuICByZXR1cm4gX19hc3NpZ24uYXBwbHkodGhpcywgYXJndW1lbnRzKTtcbn07XG52YXIgX192YWx1ZXMgPSB0aGlzICYmIHRoaXMuX192YWx1ZXMgfHwgZnVuY3Rpb24gKG8pIHtcbiAgdmFyIHMgPSB0eXBlb2YgU3ltYm9sID09PSBcImZ1bmN0aW9uXCIgJiYgU3ltYm9sLml0ZXJhdG9yLFxuICAgIG0gPSBzICYmIG9bc10sXG4gICAgaSA9IDA7XG4gIGlmIChtKSByZXR1cm4gbS5jYWxsKG8pO1xuICBpZiAobyAmJiB0eXBlb2Ygby5sZW5ndGggPT09IFwibnVtYmVyXCIpIHJldHVybiB7XG4gICAgbmV4dDogZnVuY3Rpb24gKCkge1xuICAgICAgaWYgKG8gJiYgaSA+PSBvLmxlbmd0aCkgbyA9IHZvaWQgMDtcbiAgICAgIHJldHVybiB7XG4gICAgICAgIHZhbHVlOiBvICYmIG9baSsrXSxcbiAgICAgICAgZG9uZTogIW9cbiAgICAgIH07XG4gICAgfVxuICB9O1xuICB0aHJvdyBuZXcgVHlwZUVycm9yKHMgPyBcIk9iamVjdCBpcyBub3QgaXRlcmFibGUuXCIgOiBcIlN5bWJvbC5pdGVyYXRvciBpcyBub3QgZGVmaW5lZC5cIik7XG59O1xuT2JqZWN0LmRlZmluZVByb3BlcnR5KGV4cG9ydHMsIFwiX19lc01vZHVsZVwiLCB7XG4gIHZhbHVlOiB0cnVlXG59KTtcbmV4cG9ydHMuU2FmZSA9IHZvaWQgMDtcbnZhciBPcHRpb25zX2pzXzEgPSByZXF1aXJlKFwiLi4vLi4vdXRpbC9PcHRpb25zLmpzXCIpO1xudmFyIFNhZmVNZXRob2RzX2pzXzEgPSByZXF1aXJlKFwiLi9TYWZlTWV0aG9kcy5qc1wiKTtcbnZhciBTYWZlID0gZnVuY3Rpb24gKCkge1xuICBmdW5jdGlvbiBTYWZlKGRvY3VtZW50LCBvcHRpb25zKSB7XG4gICAgdGhpcy5maWx0ZXJBdHRyaWJ1dGVzID0gbmV3IE1hcChbWydocmVmJywgJ2ZpbHRlclVSTCddLCBbJ3NyYycsICdmaWx0ZXJVUkwnXSwgWydhbHRpbWcnLCAnZmlsdGVyVVJMJ10sIFsnY2xhc3MnLCAnZmlsdGVyQ2xhc3NMaXN0J10sIFsnc3R5bGUnLCAnZmlsdGVyU3R5bGVzJ10sIFsnaWQnLCAnZmlsdGVySUQnXSwgWydmb250c2l6ZScsICdmaWx0ZXJGb250U2l6ZSddLCBbJ21hdGhzaXplJywgJ2ZpbHRlckZvbnRTaXplJ10sIFsnc2NyaXB0bWluc2l6ZScsICdmaWx0ZXJGb250U2l6ZSddLCBbJ3NjcmlwdHNpemVtdWx0aXBsaWVyJywgJ2ZpbHRlclNpemVNdWx0aXBsaWVyJ10sIFsnc2NyaXB0bGV2ZWwnLCAnZmlsdGVyU2NyaXB0TGV2ZWwnXSwgWydkYXRhLScsICdmaWx0ZXJEYXRhJ11dKTtcbiAgICB0aGlzLmZpbHRlck1ldGhvZHMgPSBfX2Fzc2lnbih7fSwgU2FmZU1ldGhvZHNfanNfMS5TYWZlTWV0aG9kcyk7XG4gICAgdGhpcy5hZGFwdG9yID0gZG9jdW1lbnQuYWRhcHRvcjtcbiAgICB0aGlzLm9wdGlvbnMgPSBvcHRpb25zO1xuICAgIHRoaXMuYWxsb3cgPSB0aGlzLm9wdGlvbnMuYWxsb3c7XG4gIH1cbiAgU2FmZS5wcm90b3R5cGUuc2FuaXRpemUgPSBmdW5jdGlvbiAobWF0aCwgZG9jdW1lbnQpIHtcbiAgICB0cnkge1xuICAgICAgbWF0aC5yb290LndhbGtUcmVlKHRoaXMuc2FuaXRpemVOb2RlLmJpbmQodGhpcykpO1xuICAgIH0gY2F0Y2ggKGVycikge1xuICAgICAgZG9jdW1lbnQub3B0aW9ucy5jb21waWxlRXJyb3IoZG9jdW1lbnQsIG1hdGgsIGVycik7XG4gICAgfVxuICB9O1xuICBTYWZlLnByb3RvdHlwZS5zYW5pdGl6ZU5vZGUgPSBmdW5jdGlvbiAobm9kZSkge1xuICAgIHZhciBlXzEsIF9hO1xuICAgIHZhciBhdHRyaWJ1dGVzID0gbm9kZS5hdHRyaWJ1dGVzLmdldEFsbEF0dHJpYnV0ZXMoKTtcbiAgICB0cnkge1xuICAgICAgZm9yICh2YXIgX2IgPSBfX3ZhbHVlcyhPYmplY3Qua2V5cyhhdHRyaWJ1dGVzKSksIF9jID0gX2IubmV4dCgpOyAhX2MuZG9uZTsgX2MgPSBfYi5uZXh0KCkpIHtcbiAgICAgICAgdmFyIGlkID0gX2MudmFsdWU7XG4gICAgICAgIHZhciBtZXRob2QgPSB0aGlzLmZpbHRlckF0dHJpYnV0ZXMuZ2V0KGlkKTtcbiAgICAgICAgaWYgKG1ldGhvZCkge1xuICAgICAgICAgIHZhciB2YWx1ZSA9IHRoaXMuZmlsdGVyTWV0aG9kc1ttZXRob2RdKHRoaXMsIGF0dHJpYnV0ZXNbaWRdKTtcbiAgICAgICAgICBpZiAodmFsdWUpIHtcbiAgICAgICAgICAgIGlmICh2YWx1ZSAhPT0gKHR5cGVvZiB2YWx1ZSA9PT0gJ251bWJlcicgPyBwYXJzZUZsb2F0KGF0dHJpYnV0ZXNbaWRdKSA6IGF0dHJpYnV0ZXNbaWRdKSkge1xuICAgICAgICAgICAgICBhdHRyaWJ1dGVzW2lkXSA9IHZhbHVlO1xuICAgICAgICAgICAgfVxuICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICBkZWxldGUgYXR0cmlidXRlc1tpZF07XG4gICAgICAgICAgfVxuICAgICAgICB9XG4gICAgICB9XG4gICAgfSBjYXRjaCAoZV8xXzEpIHtcbiAgICAgIGVfMSA9IHtcbiAgICAgICAgZXJyb3I6IGVfMV8xXG4gICAgICB9O1xuICAgIH0gZmluYWxseSB7XG4gICAgICB0cnkge1xuICAgICAgICBpZiAoX2MgJiYgIV9jLmRvbmUgJiYgKF9hID0gX2IucmV0dXJuKSkgX2EuY2FsbChfYik7XG4gICAgICB9IGZpbmFsbHkge1xuICAgICAgICBpZiAoZV8xKSB0aHJvdyBlXzEuZXJyb3I7XG4gICAgICB9XG4gICAgfVxuICB9O1xuICBTYWZlLnByb3RvdHlwZS5tbWxBdHRyaWJ1dGUgPSBmdW5jdGlvbiAoaWQsIHZhbHVlKSB7XG4gICAgaWYgKGlkID09PSAnY2xhc3MnKSByZXR1cm4gbnVsbDtcbiAgICB2YXIgbWV0aG9kID0gdGhpcy5maWx0ZXJBdHRyaWJ1dGVzLmdldChpZCk7XG4gICAgdmFyIGZpbHRlciA9IG1ldGhvZCB8fCAoaWQuc3Vic3RyKDAsIDUpID09PSAnZGF0YS0nID8gdGhpcy5maWx0ZXJBdHRyaWJ1dGVzLmdldCgnZGF0YS0nKSA6IG51bGwpO1xuICAgIGlmICghZmlsdGVyKSB7XG4gICAgICByZXR1cm4gdmFsdWU7XG4gICAgfVxuICAgIHZhciByZXN1bHQgPSB0aGlzLmZpbHRlck1ldGhvZHNbZmlsdGVyXSh0aGlzLCB2YWx1ZSwgaWQpO1xuICAgIHJldHVybiB0eXBlb2YgcmVzdWx0ID09PSAnbnVtYmVyJyB8fCB0eXBlb2YgcmVzdWx0ID09PSAnYm9vbGVhbicgPyBTdHJpbmcocmVzdWx0KSA6IHJlc3VsdDtcbiAgfTtcbiAgU2FmZS5wcm90b3R5cGUubW1sQ2xhc3NMaXN0ID0gZnVuY3Rpb24gKGxpc3QpIHtcbiAgICB2YXIgX3RoaXMgPSB0aGlzO1xuICAgIHJldHVybiBsaXN0Lm1hcChmdW5jdGlvbiAobmFtZSkge1xuICAgICAgcmV0dXJuIF90aGlzLmZpbHRlck1ldGhvZHMuZmlsdGVyQ2xhc3MoX3RoaXMsIG5hbWUpO1xuICAgIH0pLmZpbHRlcihmdW5jdGlvbiAodmFsdWUpIHtcbiAgICAgIHJldHVybiB2YWx1ZSAhPT0gbnVsbDtcbiAgICB9KTtcbiAgfTtcbiAgU2FmZS5PUFRJT05TID0ge1xuICAgIGFsbG93OiB7XG4gICAgICBVUkxzOiAnc2FmZScsXG4gICAgICBjbGFzc2VzOiAnc2FmZScsXG4gICAgICBjc3NJRHM6ICdzYWZlJyxcbiAgICAgIHN0eWxlczogJ3NhZmUnXG4gICAgfSxcbiAgICBsZW5ndGhNYXg6IDMsXG4gICAgc2NyaXB0c2l6ZW11bHRpcGxpZXJSYW5nZTogWy42LCAxXSxcbiAgICBzY3JpcHRsZXZlbFJhbmdlOiBbLTIsIDJdLFxuICAgIGNsYXNzUGF0dGVybjogL15tangtWy1hLXpBLVowLTlfLl0rJC8sXG4gICAgaWRQYXR0ZXJuOiAvXm1qeC1bLWEtekEtWjAtOV8uXSskLyxcbiAgICBkYXRhUGF0dGVybjogL15kYXRhLW1qeC0vLFxuICAgIHNhZmVQcm90b2NvbHM6ICgwLCBPcHRpb25zX2pzXzEuZXhwYW5kYWJsZSkoe1xuICAgICAgaHR0cDogdHJ1ZSxcbiAgICAgIGh0dHBzOiB0cnVlLFxuICAgICAgZmlsZTogdHJ1ZSxcbiAgICAgIGphdmFzY3JpcHQ6IGZhbHNlLFxuICAgICAgZGF0YTogZmFsc2VcbiAgICB9KSxcbiAgICBzYWZlU3R5bGVzOiAoMCwgT3B0aW9uc19qc18xLmV4cGFuZGFibGUpKHtcbiAgICAgIGNvbG9yOiB0cnVlLFxuICAgICAgYmFja2dyb3VuZENvbG9yOiB0cnVlLFxuICAgICAgYm9yZGVyOiB0cnVlLFxuICAgICAgY3Vyc29yOiB0cnVlLFxuICAgICAgbWFyZ2luOiB0cnVlLFxuICAgICAgcGFkZGluZzogdHJ1ZSxcbiAgICAgIHRleHRTaGFkb3c6IHRydWUsXG4gICAgICBmb250RmFtaWx5OiB0cnVlLFxuICAgICAgZm9udFNpemU6IHRydWUsXG4gICAgICBmb250U3R5bGU6IHRydWUsXG4gICAgICBmb250V2VpZ2h0OiB0cnVlLFxuICAgICAgb3BhY2l0eTogdHJ1ZSxcbiAgICAgIG91dGxpbmU6IHRydWVcbiAgICB9KSxcbiAgICBzdHlsZVBhcnRzOiAoMCwgT3B0aW9uc19qc18xLmV4cGFuZGFibGUpKHtcbiAgICAgIGJvcmRlcjogdHJ1ZSxcbiAgICAgIHBhZGRpbmc6IHRydWUsXG4gICAgICBtYXJnaW46IHRydWUsXG4gICAgICBvdXRsaW5lOiB0cnVlXG4gICAgfSksXG4gICAgc3R5bGVMZW5ndGhzOiAoMCwgT3B0aW9uc19qc18xLmV4cGFuZGFibGUpKHtcbiAgICAgIGJvcmRlclRvcDogJ2JvcmRlclRvcFdpZHRoJyxcbiAgICAgIGJvcmRlclJpZ2h0OiAnYm9yZGVyUmlnaHRXaWR0aCcsXG4gICAgICBib3JkZXJCb3R0b206ICdib3JkZXJCb3R0b21XaWR0aCcsXG4gICAgICBib3JkZXJMZWZ0OiAnYm9yZGVyTGVmdFdpZHRoJyxcbiAgICAgIHBhZGRpbmdUb3A6IHRydWUsXG4gICAgICBwYWRkaW5nUmlnaHQ6IHRydWUsXG4gICAgICBwYWRkaW5nQm90dG9tOiB0cnVlLFxuICAgICAgcGFkZGluZ0xlZnQ6IHRydWUsXG4gICAgICBtYXJnaW5Ub3A6IHRydWUsXG4gICAgICBtYXJnaW5SaWdodDogdHJ1ZSxcbiAgICAgIG1hcmdpbkJvdHRvbTogdHJ1ZSxcbiAgICAgIG1hcmdpbkxlZnQ6IHRydWUsXG4gICAgICBvdXRsaW5lVG9wOiB0cnVlLFxuICAgICAgb3V0bGluZVJpZ2h0OiB0cnVlLFxuICAgICAgb3V0bGluZUJvdHRvbTogdHJ1ZSxcbiAgICAgIG91dGxpbmVMZWZ0OiB0cnVlLFxuICAgICAgZm9udFNpemU6IFsuNzA3LCAxLjQ0XVxuICAgIH0pXG4gIH07XG4gIHJldHVybiBTYWZlO1xufSgpO1xuZXhwb3J0cy5TYWZlID0gU2FmZTsiLCJcInVzZSBzdHJpY3RcIjtcblxudmFyIF9fdmFsdWVzID0gdGhpcyAmJiB0aGlzLl9fdmFsdWVzIHx8IGZ1bmN0aW9uIChvKSB7XG4gIHZhciBzID0gdHlwZW9mIFN5bWJvbCA9PT0gXCJmdW5jdGlvblwiICYmIFN5bWJvbC5pdGVyYXRvcixcbiAgICBtID0gcyAmJiBvW3NdLFxuICAgIGkgPSAwO1xuICBpZiAobSkgcmV0dXJuIG0uY2FsbChvKTtcbiAgaWYgKG8gJiYgdHlwZW9mIG8ubGVuZ3RoID09PSBcIm51bWJlclwiKSByZXR1cm4ge1xuICAgIG5leHQ6IGZ1bmN0aW9uICgpIHtcbiAgICAgIGlmIChvICYmIGkgPj0gby5sZW5ndGgpIG8gPSB2b2lkIDA7XG4gICAgICByZXR1cm4ge1xuICAgICAgICB2YWx1ZTogbyAmJiBvW2krK10sXG4gICAgICAgIGRvbmU6ICFvXG4gICAgICB9O1xuICAgIH1cbiAgfTtcbiAgdGhyb3cgbmV3IFR5cGVFcnJvcihzID8gXCJPYmplY3QgaXMgbm90IGl0ZXJhYmxlLlwiIDogXCJTeW1ib2wuaXRlcmF0b3IgaXMgbm90IGRlZmluZWQuXCIpO1xufTtcbnZhciBfX3JlYWQgPSB0aGlzICYmIHRoaXMuX19yZWFkIHx8IGZ1bmN0aW9uIChvLCBuKSB7XG4gIHZhciBtID0gdHlwZW9mIFN5bWJvbCA9PT0gXCJmdW5jdGlvblwiICYmIG9bU3ltYm9sLml0ZXJhdG9yXTtcbiAgaWYgKCFtKSByZXR1cm4gbztcbiAgdmFyIGkgPSBtLmNhbGwobyksXG4gICAgcixcbiAgICBhciA9IFtdLFxuICAgIGU7XG4gIHRyeSB7XG4gICAgd2hpbGUgKChuID09PSB2b2lkIDAgfHwgbi0tID4gMCkgJiYgIShyID0gaS5uZXh0KCkpLmRvbmUpIGFyLnB1c2goci52YWx1ZSk7XG4gIH0gY2F0Y2ggKGVycm9yKSB7XG4gICAgZSA9IHtcbiAgICAgIGVycm9yOiBlcnJvclxuICAgIH07XG4gIH0gZmluYWxseSB7XG4gICAgdHJ5IHtcbiAgICAgIGlmIChyICYmICFyLmRvbmUgJiYgKG0gPSBpW1wicmV0dXJuXCJdKSkgbS5jYWxsKGkpO1xuICAgIH0gZmluYWxseSB7XG4gICAgICBpZiAoZSkgdGhyb3cgZS5lcnJvcjtcbiAgICB9XG4gIH1cbiAgcmV0dXJuIGFyO1xufTtcbnZhciBfX3NwcmVhZEFycmF5ID0gdGhpcyAmJiB0aGlzLl9fc3ByZWFkQXJyYXkgfHwgZnVuY3Rpb24gKHRvLCBmcm9tLCBwYWNrKSB7XG4gIGlmIChwYWNrIHx8IGFyZ3VtZW50cy5sZW5ndGggPT09IDIpIGZvciAodmFyIGkgPSAwLCBsID0gZnJvbS5sZW5ndGgsIGFyOyBpIDwgbDsgaSsrKSB7XG4gICAgaWYgKGFyIHx8ICEoaSBpbiBmcm9tKSkge1xuICAgICAgaWYgKCFhcikgYXIgPSBBcnJheS5wcm90b3R5cGUuc2xpY2UuY2FsbChmcm9tLCAwLCBpKTtcbiAgICAgIGFyW2ldID0gZnJvbVtpXTtcbiAgICB9XG4gIH1cbiAgcmV0dXJuIHRvLmNvbmNhdChhciB8fCBBcnJheS5wcm90b3R5cGUuc2xpY2UuY2FsbChmcm9tKSk7XG59O1xuT2JqZWN0LmRlZmluZVByb3BlcnR5KGV4cG9ydHMsIFwiX19lc01vZHVsZVwiLCB7XG4gIHZhbHVlOiB0cnVlXG59KTtcbmV4cG9ydHMubG9va3VwID0gZXhwb3J0cy5zZXBhcmF0ZU9wdGlvbnMgPSBleHBvcnRzLnNlbGVjdE9wdGlvbnNGcm9tS2V5cyA9IGV4cG9ydHMuc2VsZWN0T3B0aW9ucyA9IGV4cG9ydHMudXNlck9wdGlvbnMgPSBleHBvcnRzLmRlZmF1bHRPcHRpb25zID0gZXhwb3J0cy5pbnNlcnQgPSBleHBvcnRzLmNvcHkgPSBleHBvcnRzLmtleXMgPSBleHBvcnRzLm1ha2VBcnJheSA9IGV4cG9ydHMuZXhwYW5kYWJsZSA9IGV4cG9ydHMuRXhwYW5kYWJsZSA9IGV4cG9ydHMuT1BUSU9OUyA9IGV4cG9ydHMuUkVNT1ZFID0gZXhwb3J0cy5BUFBFTkQgPSBleHBvcnRzLmlzT2JqZWN0ID0gdm9pZCAwO1xudmFyIE9CSkVDVCA9IHt9LmNvbnN0cnVjdG9yO1xuZnVuY3Rpb24gaXNPYmplY3Qob2JqKSB7XG4gIHJldHVybiB0eXBlb2Ygb2JqID09PSAnb2JqZWN0JyAmJiBvYmogIT09IG51bGwgJiYgKG9iai5jb25zdHJ1Y3RvciA9PT0gT0JKRUNUIHx8IG9iai5jb25zdHJ1Y3RvciA9PT0gRXhwYW5kYWJsZSk7XG59XG5leHBvcnRzLmlzT2JqZWN0ID0gaXNPYmplY3Q7XG5leHBvcnRzLkFQUEVORCA9ICdbK10nO1xuZXhwb3J0cy5SRU1PVkUgPSAnWy1dJztcbmV4cG9ydHMuT1BUSU9OUyA9IHtcbiAgaW52YWxpZE9wdGlvbjogJ3dhcm4nLFxuICBvcHRpb25FcnJvcjogZnVuY3Rpb24gKG1lc3NhZ2UsIF9rZXkpIHtcbiAgICBpZiAoZXhwb3J0cy5PUFRJT05TLmludmFsaWRPcHRpb24gPT09ICdmYXRhbCcpIHtcbiAgICAgIHRocm93IG5ldyBFcnJvcihtZXNzYWdlKTtcbiAgICB9XG4gICAgY29uc29sZS53YXJuKCdNYXRoSmF4OiAnICsgbWVzc2FnZSk7XG4gIH1cbn07XG52YXIgRXhwYW5kYWJsZSA9IGZ1bmN0aW9uICgpIHtcbiAgZnVuY3Rpb24gRXhwYW5kYWJsZSgpIHt9XG4gIHJldHVybiBFeHBhbmRhYmxlO1xufSgpO1xuZXhwb3J0cy5FeHBhbmRhYmxlID0gRXhwYW5kYWJsZTtcbmZ1bmN0aW9uIGV4cGFuZGFibGUoZGVmKSB7XG4gIHJldHVybiBPYmplY3QuYXNzaWduKE9iamVjdC5jcmVhdGUoRXhwYW5kYWJsZS5wcm90b3R5cGUpLCBkZWYpO1xufVxuZXhwb3J0cy5leHBhbmRhYmxlID0gZXhwYW5kYWJsZTtcbmZ1bmN0aW9uIG1ha2VBcnJheSh4KSB7XG4gIHJldHVybiBBcnJheS5pc0FycmF5KHgpID8geCA6IFt4XTtcbn1cbmV4cG9ydHMubWFrZUFycmF5ID0gbWFrZUFycmF5O1xuZnVuY3Rpb24ga2V5cyhkZWYpIHtcbiAgaWYgKCFkZWYpIHtcbiAgICByZXR1cm4gW107XG4gIH1cbiAgcmV0dXJuIE9iamVjdC5rZXlzKGRlZikuY29uY2F0KE9iamVjdC5nZXRPd25Qcm9wZXJ0eVN5bWJvbHMoZGVmKSk7XG59XG5leHBvcnRzLmtleXMgPSBrZXlzO1xuZnVuY3Rpb24gY29weShkZWYpIHtcbiAgdmFyIGVfMSwgX2E7XG4gIHZhciBwcm9wcyA9IHt9O1xuICB0cnkge1xuICAgIGZvciAodmFyIF9iID0gX192YWx1ZXMoa2V5cyhkZWYpKSwgX2MgPSBfYi5uZXh0KCk7ICFfYy5kb25lOyBfYyA9IF9iLm5leHQoKSkge1xuICAgICAgdmFyIGtleSA9IF9jLnZhbHVlO1xuICAgICAgdmFyIHByb3AgPSBPYmplY3QuZ2V0T3duUHJvcGVydHlEZXNjcmlwdG9yKGRlZiwga2V5KTtcbiAgICAgIHZhciB2YWx1ZSA9IHByb3AudmFsdWU7XG4gICAgICBpZiAoQXJyYXkuaXNBcnJheSh2YWx1ZSkpIHtcbiAgICAgICAgcHJvcC52YWx1ZSA9IGluc2VydChbXSwgdmFsdWUsIGZhbHNlKTtcbiAgICAgIH0gZWxzZSBpZiAoaXNPYmplY3QodmFsdWUpKSB7XG4gICAgICAgIHByb3AudmFsdWUgPSBjb3B5KHZhbHVlKTtcbiAgICAgIH1cbiAgICAgIGlmIChwcm9wLmVudW1lcmFibGUpIHtcbiAgICAgICAgcHJvcHNba2V5XSA9IHByb3A7XG4gICAgICB9XG4gICAgfVxuICB9IGNhdGNoIChlXzFfMSkge1xuICAgIGVfMSA9IHtcbiAgICAgIGVycm9yOiBlXzFfMVxuICAgIH07XG4gIH0gZmluYWxseSB7XG4gICAgdHJ5IHtcbiAgICAgIGlmIChfYyAmJiAhX2MuZG9uZSAmJiAoX2EgPSBfYi5yZXR1cm4pKSBfYS5jYWxsKF9iKTtcbiAgICB9IGZpbmFsbHkge1xuICAgICAgaWYgKGVfMSkgdGhyb3cgZV8xLmVycm9yO1xuICAgIH1cbiAgfVxuICByZXR1cm4gT2JqZWN0LmRlZmluZVByb3BlcnRpZXMoZGVmLmNvbnN0cnVjdG9yID09PSBFeHBhbmRhYmxlID8gZXhwYW5kYWJsZSh7fSkgOiB7fSwgcHJvcHMpO1xufVxuZXhwb3J0cy5jb3B5ID0gY29weTtcbmZ1bmN0aW9uIGluc2VydChkc3QsIHNyYywgd2Fybikge1xuICB2YXIgZV8yLCBfYTtcbiAgaWYgKHdhcm4gPT09IHZvaWQgMCkge1xuICAgIHdhcm4gPSB0cnVlO1xuICB9XG4gIHZhciBfbG9vcF8xID0gZnVuY3Rpb24gKGtleSkge1xuICAgIGlmICh3YXJuICYmIGRzdFtrZXldID09PSB1bmRlZmluZWQgJiYgZHN0LmNvbnN0cnVjdG9yICE9PSBFeHBhbmRhYmxlKSB7XG4gICAgICBpZiAodHlwZW9mIGtleSA9PT0gJ3N5bWJvbCcpIHtcbiAgICAgICAga2V5ID0ga2V5LnRvU3RyaW5nKCk7XG4gICAgICB9XG4gICAgICBleHBvcnRzLk9QVElPTlMub3B0aW9uRXJyb3IoXCJJbnZhbGlkIG9wdGlvbiBcXFwiXCIuY29uY2F0KGtleSwgXCJcXFwiIChubyBkZWZhdWx0IHZhbHVlKS5cIiksIGtleSk7XG4gICAgICByZXR1cm4gXCJjb250aW51ZVwiO1xuICAgIH1cbiAgICB2YXIgc3ZhbCA9IHNyY1trZXldLFxuICAgICAgZHZhbCA9IGRzdFtrZXldO1xuICAgIGlmIChpc09iamVjdChzdmFsKSAmJiBkdmFsICE9PSBudWxsICYmICh0eXBlb2YgZHZhbCA9PT0gJ29iamVjdCcgfHwgdHlwZW9mIGR2YWwgPT09ICdmdW5jdGlvbicpKSB7XG4gICAgICB2YXIgaWRzID0ga2V5cyhzdmFsKTtcbiAgICAgIGlmIChBcnJheS5pc0FycmF5KGR2YWwpICYmIChpZHMubGVuZ3RoID09PSAxICYmIChpZHNbMF0gPT09IGV4cG9ydHMuQVBQRU5EIHx8IGlkc1swXSA9PT0gZXhwb3J0cy5SRU1PVkUpICYmIEFycmF5LmlzQXJyYXkoc3ZhbFtpZHNbMF1dKSB8fCBpZHMubGVuZ3RoID09PSAyICYmIGlkcy5zb3J0KCkuam9pbignLCcpID09PSBleHBvcnRzLkFQUEVORCArICcsJyArIGV4cG9ydHMuUkVNT1ZFICYmIEFycmF5LmlzQXJyYXkoc3ZhbFtleHBvcnRzLkFQUEVORF0pICYmIEFycmF5LmlzQXJyYXkoc3ZhbFtleHBvcnRzLlJFTU9WRV0pKSkge1xuICAgICAgICBpZiAoc3ZhbFtleHBvcnRzLlJFTU9WRV0pIHtcbiAgICAgICAgICBkdmFsID0gZHN0W2tleV0gPSBkdmFsLmZpbHRlcihmdW5jdGlvbiAoeCkge1xuICAgICAgICAgICAgcmV0dXJuIHN2YWxbZXhwb3J0cy5SRU1PVkVdLmluZGV4T2YoeCkgPCAwO1xuICAgICAgICAgIH0pO1xuICAgICAgICB9XG4gICAgICAgIGlmIChzdmFsW2V4cG9ydHMuQVBQRU5EXSkge1xuICAgICAgICAgIGRzdFtrZXldID0gX19zcHJlYWRBcnJheShfX3NwcmVhZEFycmF5KFtdLCBfX3JlYWQoZHZhbCksIGZhbHNlKSwgX19yZWFkKHN2YWxbZXhwb3J0cy5BUFBFTkRdKSwgZmFsc2UpO1xuICAgICAgICB9XG4gICAgICB9IGVsc2Uge1xuICAgICAgICBpbnNlcnQoZHZhbCwgc3ZhbCwgd2Fybik7XG4gICAgICB9XG4gICAgfSBlbHNlIGlmIChBcnJheS5pc0FycmF5KHN2YWwpKSB7XG4gICAgICBkc3Rba2V5XSA9IFtdO1xuICAgICAgaW5zZXJ0KGRzdFtrZXldLCBzdmFsLCBmYWxzZSk7XG4gICAgfSBlbHNlIGlmIChpc09iamVjdChzdmFsKSkge1xuICAgICAgZHN0W2tleV0gPSBjb3B5KHN2YWwpO1xuICAgIH0gZWxzZSB7XG4gICAgICBkc3Rba2V5XSA9IHN2YWw7XG4gICAgfVxuICB9O1xuICB0cnkge1xuICAgIGZvciAodmFyIF9iID0gX192YWx1ZXMoa2V5cyhzcmMpKSwgX2MgPSBfYi5uZXh0KCk7ICFfYy5kb25lOyBfYyA9IF9iLm5leHQoKSkge1xuICAgICAgdmFyIGtleSA9IF9jLnZhbHVlO1xuICAgICAgX2xvb3BfMShrZXkpO1xuICAgIH1cbiAgfSBjYXRjaCAoZV8yXzEpIHtcbiAgICBlXzIgPSB7XG4gICAgICBlcnJvcjogZV8yXzFcbiAgICB9O1xuICB9IGZpbmFsbHkge1xuICAgIHRyeSB7XG4gICAgICBpZiAoX2MgJiYgIV9jLmRvbmUgJiYgKF9hID0gX2IucmV0dXJuKSkgX2EuY2FsbChfYik7XG4gICAgfSBmaW5hbGx5IHtcbiAgICAgIGlmIChlXzIpIHRocm93IGVfMi5lcnJvcjtcbiAgICB9XG4gIH1cbiAgcmV0dXJuIGRzdDtcbn1cbmV4cG9ydHMuaW5zZXJ0ID0gaW5zZXJ0O1xuZnVuY3Rpb24gZGVmYXVsdE9wdGlvbnMob3B0aW9ucykge1xuICB2YXIgZGVmcyA9IFtdO1xuICBmb3IgKHZhciBfaSA9IDE7IF9pIDwgYXJndW1lbnRzLmxlbmd0aDsgX2krKykge1xuICAgIGRlZnNbX2kgLSAxXSA9IGFyZ3VtZW50c1tfaV07XG4gIH1cbiAgZGVmcy5mb3JFYWNoKGZ1bmN0aW9uIChkZWYpIHtcbiAgICByZXR1cm4gaW5zZXJ0KG9wdGlvbnMsIGRlZiwgZmFsc2UpO1xuICB9KTtcbiAgcmV0dXJuIG9wdGlvbnM7XG59XG5leHBvcnRzLmRlZmF1bHRPcHRpb25zID0gZGVmYXVsdE9wdGlvbnM7XG5mdW5jdGlvbiB1c2VyT3B0aW9ucyhvcHRpb25zKSB7XG4gIHZhciBkZWZzID0gW107XG4gIGZvciAodmFyIF9pID0gMTsgX2kgPCBhcmd1bWVudHMubGVuZ3RoOyBfaSsrKSB7XG4gICAgZGVmc1tfaSAtIDFdID0gYXJndW1lbnRzW19pXTtcbiAgfVxuICBkZWZzLmZvckVhY2goZnVuY3Rpb24gKGRlZikge1xuICAgIHJldHVybiBpbnNlcnQob3B0aW9ucywgZGVmLCB0cnVlKTtcbiAgfSk7XG4gIHJldHVybiBvcHRpb25zO1xufVxuZXhwb3J0cy51c2VyT3B0aW9ucyA9IHVzZXJPcHRpb25zO1xuZnVuY3Rpb24gc2VsZWN0T3B0aW9ucyhvcHRpb25zKSB7XG4gIHZhciBlXzMsIF9hO1xuICB2YXIga2V5cyA9IFtdO1xuICBmb3IgKHZhciBfaSA9IDE7IF9pIDwgYXJndW1lbnRzLmxlbmd0aDsgX2krKykge1xuICAgIGtleXNbX2kgLSAxXSA9IGFyZ3VtZW50c1tfaV07XG4gIH1cbiAgdmFyIHN1YnNldCA9IHt9O1xuICB0cnkge1xuICAgIGZvciAodmFyIGtleXNfMSA9IF9fdmFsdWVzKGtleXMpLCBrZXlzXzFfMSA9IGtleXNfMS5uZXh0KCk7ICFrZXlzXzFfMS5kb25lOyBrZXlzXzFfMSA9IGtleXNfMS5uZXh0KCkpIHtcbiAgICAgIHZhciBrZXkgPSBrZXlzXzFfMS52YWx1ZTtcbiAgICAgIGlmIChvcHRpb25zLmhhc093blByb3BlcnR5KGtleSkpIHtcbiAgICAgICAgc3Vic2V0W2tleV0gPSBvcHRpb25zW2tleV07XG4gICAgICB9XG4gICAgfVxuICB9IGNhdGNoIChlXzNfMSkge1xuICAgIGVfMyA9IHtcbiAgICAgIGVycm9yOiBlXzNfMVxuICAgIH07XG4gIH0gZmluYWxseSB7XG4gICAgdHJ5IHtcbiAgICAgIGlmIChrZXlzXzFfMSAmJiAha2V5c18xXzEuZG9uZSAmJiAoX2EgPSBrZXlzXzEucmV0dXJuKSkgX2EuY2FsbChrZXlzXzEpO1xuICAgIH0gZmluYWxseSB7XG4gICAgICBpZiAoZV8zKSB0aHJvdyBlXzMuZXJyb3I7XG4gICAgfVxuICB9XG4gIHJldHVybiBzdWJzZXQ7XG59XG5leHBvcnRzLnNlbGVjdE9wdGlvbnMgPSBzZWxlY3RPcHRpb25zO1xuZnVuY3Rpb24gc2VsZWN0T3B0aW9uc0Zyb21LZXlzKG9wdGlvbnMsIG9iamVjdCkge1xuICByZXR1cm4gc2VsZWN0T3B0aW9ucy5hcHBseSh2b2lkIDAsIF9fc3ByZWFkQXJyYXkoW29wdGlvbnNdLCBfX3JlYWQoT2JqZWN0LmtleXMob2JqZWN0KSksIGZhbHNlKSk7XG59XG5leHBvcnRzLnNlbGVjdE9wdGlvbnNGcm9tS2V5cyA9IHNlbGVjdE9wdGlvbnNGcm9tS2V5cztcbmZ1bmN0aW9uIHNlcGFyYXRlT3B0aW9ucyhvcHRpb25zKSB7XG4gIHZhciBlXzQsIF9hLCBlXzUsIF9iO1xuICB2YXIgb2JqZWN0cyA9IFtdO1xuICBmb3IgKHZhciBfaSA9IDE7IF9pIDwgYXJndW1lbnRzLmxlbmd0aDsgX2krKykge1xuICAgIG9iamVjdHNbX2kgLSAxXSA9IGFyZ3VtZW50c1tfaV07XG4gIH1cbiAgdmFyIHJlc3VsdHMgPSBbXTtcbiAgdHJ5IHtcbiAgICBmb3IgKHZhciBvYmplY3RzXzEgPSBfX3ZhbHVlcyhvYmplY3RzKSwgb2JqZWN0c18xXzEgPSBvYmplY3RzXzEubmV4dCgpOyAhb2JqZWN0c18xXzEuZG9uZTsgb2JqZWN0c18xXzEgPSBvYmplY3RzXzEubmV4dCgpKSB7XG4gICAgICB2YXIgb2JqZWN0ID0gb2JqZWN0c18xXzEudmFsdWU7XG4gICAgICB2YXIgZXhpc3RzID0ge30sXG4gICAgICAgIG1pc3NpbmcgPSB7fTtcbiAgICAgIHRyeSB7XG4gICAgICAgIGZvciAodmFyIF9jID0gKGVfNSA9IHZvaWQgMCwgX192YWx1ZXMoT2JqZWN0LmtleXMob3B0aW9ucyB8fCB7fSkpKSwgX2QgPSBfYy5uZXh0KCk7ICFfZC5kb25lOyBfZCA9IF9jLm5leHQoKSkge1xuICAgICAgICAgIHZhciBrZXkgPSBfZC52YWx1ZTtcbiAgICAgICAgICAob2JqZWN0W2tleV0gPT09IHVuZGVmaW5lZCA/IG1pc3NpbmcgOiBleGlzdHMpW2tleV0gPSBvcHRpb25zW2tleV07XG4gICAgICAgIH1cbiAgICAgIH0gY2F0Y2ggKGVfNV8xKSB7XG4gICAgICAgIGVfNSA9IHtcbiAgICAgICAgICBlcnJvcjogZV81XzFcbiAgICAgICAgfTtcbiAgICAgIH0gZmluYWxseSB7XG4gICAgICAgIHRyeSB7XG4gICAgICAgICAgaWYgKF9kICYmICFfZC5kb25lICYmIChfYiA9IF9jLnJldHVybikpIF9iLmNhbGwoX2MpO1xuICAgICAgICB9IGZpbmFsbHkge1xuICAgICAgICAgIGlmIChlXzUpIHRocm93IGVfNS5lcnJvcjtcbiAgICAgICAgfVxuICAgICAgfVxuICAgICAgcmVzdWx0cy5wdXNoKGV4aXN0cyk7XG4gICAgICBvcHRpb25zID0gbWlzc2luZztcbiAgICB9XG4gIH0gY2F0Y2ggKGVfNF8xKSB7XG4gICAgZV80ID0ge1xuICAgICAgZXJyb3I6IGVfNF8xXG4gICAgfTtcbiAgfSBmaW5hbGx5IHtcbiAgICB0cnkge1xuICAgICAgaWYgKG9iamVjdHNfMV8xICYmICFvYmplY3RzXzFfMS5kb25lICYmIChfYSA9IG9iamVjdHNfMS5yZXR1cm4pKSBfYS5jYWxsKG9iamVjdHNfMSk7XG4gICAgfSBmaW5hbGx5IHtcbiAgICAgIGlmIChlXzQpIHRocm93IGVfNC5lcnJvcjtcbiAgICB9XG4gIH1cbiAgcmVzdWx0cy51bnNoaWZ0KG9wdGlvbnMpO1xuICByZXR1cm4gcmVzdWx0cztcbn1cbmV4cG9ydHMuc2VwYXJhdGVPcHRpb25zID0gc2VwYXJhdGVPcHRpb25zO1xuZnVuY3Rpb24gbG9va3VwKG5hbWUsIGxvb2t1cCwgZGVmKSB7XG4gIGlmIChkZWYgPT09IHZvaWQgMCkge1xuICAgIGRlZiA9IG51bGw7XG4gIH1cbiAgcmV0dXJuIGxvb2t1cC5oYXNPd25Qcm9wZXJ0eShuYW1lKSA/IGxvb2t1cFtuYW1lXSA6IGRlZjtcbn1cbmV4cG9ydHMubG9va3VwID0gbG9va3VwOyIsIlwidXNlIHN0cmljdFwiO1xuXG5PYmplY3QuZGVmaW5lUHJvcGVydHkoZXhwb3J0cywgXCJfX2VzTW9kdWxlXCIsIHtcbiAgdmFsdWU6IHRydWVcbn0pO1xuZXhwb3J0cy5weCA9IGV4cG9ydHMuZW1Sb3VuZGVkID0gZXhwb3J0cy5lbSA9IGV4cG9ydHMucGVyY2VudCA9IGV4cG9ydHMubGVuZ3RoMmVtID0gZXhwb3J0cy5NQVRIU1BBQ0UgPSBleHBvcnRzLlJFTFVOSVRTID0gZXhwb3J0cy5VTklUUyA9IGV4cG9ydHMuQklHRElNRU4gPSB2b2lkIDA7XG5leHBvcnRzLkJJR0RJTUVOID0gMTAwMDAwMDtcbmV4cG9ydHMuVU5JVFMgPSB7XG4gIHB4OiAxLFxuICAnaW4nOiA5NixcbiAgY206IDk2IC8gMi41NCxcbiAgbW06IDk2IC8gMjUuNFxufTtcbmV4cG9ydHMuUkVMVU5JVFMgPSB7XG4gIGVtOiAxLFxuICBleDogLjQzMSxcbiAgcHQ6IDEgLyAxMCxcbiAgcGM6IDEyIC8gMTAsXG4gIG11OiAxIC8gMThcbn07XG5leHBvcnRzLk1BVEhTUEFDRSA9IHtcbiAgdmVyeXZlcnl0aGlubWF0aHNwYWNlOiAxIC8gMTgsXG4gIHZlcnl0aGlubWF0aHNwYWNlOiAyIC8gMTgsXG4gIHRoaW5tYXRoc3BhY2U6IDMgLyAxOCxcbiAgbWVkaXVtbWF0aHNwYWNlOiA0IC8gMTgsXG4gIHRoaWNrbWF0aHNwYWNlOiA1IC8gMTgsXG4gIHZlcnl0aGlja21hdGhzcGFjZTogNiAvIDE4LFxuICB2ZXJ5dmVyeXRoaWNrbWF0aHNwYWNlOiA3IC8gMTgsXG4gIG5lZ2F0aXZldmVyeXZlcnl0aGlubWF0aHNwYWNlOiAtMSAvIDE4LFxuICBuZWdhdGl2ZXZlcnl0aGlubWF0aHNwYWNlOiAtMiAvIDE4LFxuICBuZWdhdGl2ZXRoaW5tYXRoc3BhY2U6IC0zIC8gMTgsXG4gIG5lZ2F0aXZlbWVkaXVtbWF0aHNwYWNlOiAtNCAvIDE4LFxuICBuZWdhdGl2ZXRoaWNrbWF0aHNwYWNlOiAtNSAvIDE4LFxuICBuZWdhdGl2ZXZlcnl0aGlja21hdGhzcGFjZTogLTYgLyAxOCxcbiAgbmVnYXRpdmV2ZXJ5dmVyeXRoaWNrbWF0aHNwYWNlOiAtNyAvIDE4LFxuICB0aGluOiAuMDQsXG4gIG1lZGl1bTogLjA2LFxuICB0aGljazogLjEsXG4gIG5vcm1hbDogMSxcbiAgYmlnOiAyLFxuICBzbWFsbDogMSAvIE1hdGguc3FydCgyKSxcbiAgaW5maW5pdHk6IGV4cG9ydHMuQklHRElNRU5cbn07XG5mdW5jdGlvbiBsZW5ndGgyZW0obGVuZ3RoLCBzaXplLCBzY2FsZSwgZW0pIHtcbiAgaWYgKHNpemUgPT09IHZvaWQgMCkge1xuICAgIHNpemUgPSAwO1xuICB9XG4gIGlmIChzY2FsZSA9PT0gdm9pZCAwKSB7XG4gICAgc2NhbGUgPSAxO1xuICB9XG4gIGlmIChlbSA9PT0gdm9pZCAwKSB7XG4gICAgZW0gPSAxNjtcbiAgfVxuICBpZiAodHlwZW9mIGxlbmd0aCAhPT0gJ3N0cmluZycpIHtcbiAgICBsZW5ndGggPSBTdHJpbmcobGVuZ3RoKTtcbiAgfVxuICBpZiAobGVuZ3RoID09PSAnJyB8fCBsZW5ndGggPT0gbnVsbCkge1xuICAgIHJldHVybiBzaXplO1xuICB9XG4gIGlmIChleHBvcnRzLk1BVEhTUEFDRVtsZW5ndGhdKSB7XG4gICAgcmV0dXJuIGV4cG9ydHMuTUFUSFNQQUNFW2xlbmd0aF07XG4gIH1cbiAgdmFyIG1hdGNoID0gbGVuZ3RoLm1hdGNoKC9eXFxzKihbLStdPyg/OlxcLlxcZCt8XFxkKyg/OlxcLlxcZCopPykpPyhwdHxlbXxleHxtdXxweHxwY3xpbnxtbXxjbXwlKT8vKTtcbiAgaWYgKCFtYXRjaCkge1xuICAgIHJldHVybiBzaXplO1xuICB9XG4gIHZhciBtID0gcGFyc2VGbG9hdChtYXRjaFsxXSB8fCAnMScpLFxuICAgIHVuaXQgPSBtYXRjaFsyXTtcbiAgaWYgKGV4cG9ydHMuVU5JVFMuaGFzT3duUHJvcGVydHkodW5pdCkpIHtcbiAgICByZXR1cm4gbSAqIGV4cG9ydHMuVU5JVFNbdW5pdF0gLyBlbSAvIHNjYWxlO1xuICB9XG4gIGlmIChleHBvcnRzLlJFTFVOSVRTLmhhc093blByb3BlcnR5KHVuaXQpKSB7XG4gICAgcmV0dXJuIG0gKiBleHBvcnRzLlJFTFVOSVRTW3VuaXRdO1xuICB9XG4gIGlmICh1bml0ID09PSAnJScpIHtcbiAgICByZXR1cm4gbSAvIDEwMCAqIHNpemU7XG4gIH1cbiAgcmV0dXJuIG0gKiBzaXplO1xufVxuZXhwb3J0cy5sZW5ndGgyZW0gPSBsZW5ndGgyZW07XG5mdW5jdGlvbiBwZXJjZW50KG0pIHtcbiAgcmV0dXJuICgxMDAgKiBtKS50b0ZpeGVkKDEpLnJlcGxhY2UoL1xcLj8wKyQvLCAnJykgKyAnJSc7XG59XG5leHBvcnRzLnBlcmNlbnQgPSBwZXJjZW50O1xuZnVuY3Rpb24gZW0obSkge1xuICBpZiAoTWF0aC5hYnMobSkgPCAuMDAxKSByZXR1cm4gJzAnO1xuICByZXR1cm4gbS50b0ZpeGVkKDMpLnJlcGxhY2UoL1xcLj8wKyQvLCAnJykgKyAnZW0nO1xufVxuZXhwb3J0cy5lbSA9IGVtO1xuZnVuY3Rpb24gZW1Sb3VuZGVkKG0sIGVtKSB7XG4gIGlmIChlbSA9PT0gdm9pZCAwKSB7XG4gICAgZW0gPSAxNjtcbiAgfVxuICBtID0gKE1hdGgucm91bmQobSAqIGVtKSArIC4wNSkgLyBlbTtcbiAgaWYgKE1hdGguYWJzKG0pIDwgLjAwMSkgcmV0dXJuICcwZW0nO1xuICByZXR1cm4gbS50b0ZpeGVkKDMpLnJlcGxhY2UoL1xcLj8wKyQvLCAnJykgKyAnZW0nO1xufVxuZXhwb3J0cy5lbVJvdW5kZWQgPSBlbVJvdW5kZWQ7XG5mdW5jdGlvbiBweChtLCBNLCBlbSkge1xuICBpZiAoTSA9PT0gdm9pZCAwKSB7XG4gICAgTSA9IC1leHBvcnRzLkJJR0RJTUVOO1xuICB9XG4gIGlmIChlbSA9PT0gdm9pZCAwKSB7XG4gICAgZW0gPSAxNjtcbiAgfVxuICBtICo9IGVtO1xuICBpZiAoTSAmJiBtIDwgTSkgbSA9IE07XG4gIGlmIChNYXRoLmFicyhtKSA8IC4xKSByZXR1cm4gJzAnO1xuICByZXR1cm4gbS50b0ZpeGVkKDEpLnJlcGxhY2UoL1xcLjAkLywgJycpICsgJ3B4Jztcbn1cbmV4cG9ydHMucHggPSBweDsiXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=
"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[8790],{

/***/ 72177:
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {



Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports.AbstractFindMath = void 0;
var Options_js_1 = __webpack_require__(62704);
var AbstractFindMath = function () {
  function AbstractFindMath(options) {
    var CLASS = this.constructor;
    this.options = (0, Options_js_1.userOptions)((0, Options_js_1.defaultOptions)({}, CLASS.OPTIONS), options);
  }
  AbstractFindMath.OPTIONS = {};
  return AbstractFindMath;
}();
exports.AbstractFindMath = AbstractFindMath;

/***/ }),

/***/ 87261:
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {



Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports.AbstractInputJax = void 0;
var Options_js_1 = __webpack_require__(62704);
var FunctionList_js_1 = __webpack_require__(58235);
var AbstractInputJax = function () {
  function AbstractInputJax(options) {
    if (options === void 0) {
      options = {};
    }
    this.adaptor = null;
    this.mmlFactory = null;
    var CLASS = this.constructor;
    this.options = (0, Options_js_1.userOptions)((0, Options_js_1.defaultOptions)({}, CLASS.OPTIONS), options);
    this.preFilters = new FunctionList_js_1.FunctionList();
    this.postFilters = new FunctionList_js_1.FunctionList();
  }
  Object.defineProperty(AbstractInputJax.prototype, "name", {
    get: function () {
      return this.constructor.NAME;
    },
    enumerable: false,
    configurable: true
  });
  AbstractInputJax.prototype.setAdaptor = function (adaptor) {
    this.adaptor = adaptor;
  };
  AbstractInputJax.prototype.setMmlFactory = function (mmlFactory) {
    this.mmlFactory = mmlFactory;
  };
  AbstractInputJax.prototype.initialize = function () {};
  AbstractInputJax.prototype.reset = function () {
    var _args = [];
    for (var _i = 0; _i < arguments.length; _i++) {
      _args[_i] = arguments[_i];
    }
  };
  Object.defineProperty(AbstractInputJax.prototype, "processStrings", {
    get: function () {
      return true;
    },
    enumerable: false,
    configurable: true
  });
  AbstractInputJax.prototype.findMath = function (_node, _options) {
    return [];
  };
  AbstractInputJax.prototype.executeFilters = function (filters, math, document, data) {
    var args = {
      math: math,
      document: document,
      data: data
    };
    filters.execute(args);
    return args.data;
  };
  AbstractInputJax.NAME = 'generic';
  AbstractInputJax.OPTIONS = {};
  return AbstractInputJax;
}();
exports.AbstractInputJax = AbstractInputJax;

/***/ }),

/***/ 57714:
/***/ ((__unused_webpack_module, exports) => {



Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports.newState = exports.STATE = exports.AbstractMathItem = exports.protoItem = void 0;
function protoItem(open, math, close, n, start, end, display) {
  if (display === void 0) {
    display = null;
  }
  var item = {
    open: open,
    math: math,
    close: close,
    n: n,
    start: {
      n: start
    },
    end: {
      n: end
    },
    display: display
  };
  return item;
}
exports.protoItem = protoItem;
var AbstractMathItem = function () {
  function AbstractMathItem(math, jax, display, start, end) {
    if (display === void 0) {
      display = true;
    }
    if (start === void 0) {
      start = {
        i: 0,
        n: 0,
        delim: ''
      };
    }
    if (end === void 0) {
      end = {
        i: 0,
        n: 0,
        delim: ''
      };
    }
    this.root = null;
    this.typesetRoot = null;
    this.metrics = {};
    this.inputData = {};
    this.outputData = {};
    this._state = exports.STATE.UNPROCESSED;
    this.math = math;
    this.inputJax = jax;
    this.display = display;
    this.start = start;
    this.end = end;
    this.root = null;
    this.typesetRoot = null;
    this.metrics = {};
    this.inputData = {};
    this.outputData = {};
  }
  Object.defineProperty(AbstractMathItem.prototype, "isEscaped", {
    get: function () {
      return this.display === null;
    },
    enumerable: false,
    configurable: true
  });
  AbstractMathItem.prototype.render = function (document) {
    document.renderActions.renderMath(this, document);
  };
  AbstractMathItem.prototype.rerender = function (document, start) {
    if (start === void 0) {
      start = exports.STATE.RERENDER;
    }
    if (this.state() >= start) {
      this.state(start - 1);
    }
    document.renderActions.renderMath(this, document, start);
  };
  AbstractMathItem.prototype.convert = function (document, end) {
    if (end === void 0) {
      end = exports.STATE.LAST;
    }
    document.renderActions.renderConvert(this, document, end);
  };
  AbstractMathItem.prototype.compile = function (document) {
    if (this.state() < exports.STATE.COMPILED) {
      this.root = this.inputJax.compile(this, document);
      this.state(exports.STATE.COMPILED);
    }
  };
  AbstractMathItem.prototype.typeset = function (document) {
    if (this.state() < exports.STATE.TYPESET) {
      this.typesetRoot = document.outputJax[this.isEscaped ? 'escaped' : 'typeset'](this, document);
      this.state(exports.STATE.TYPESET);
    }
  };
  AbstractMathItem.prototype.updateDocument = function (_document) {};
  AbstractMathItem.prototype.removeFromDocument = function (_restore) {
    if (_restore === void 0) {
      _restore = false;
    }
  };
  AbstractMathItem.prototype.setMetrics = function (em, ex, cwidth, lwidth, scale) {
    this.metrics = {
      em: em,
      ex: ex,
      containerWidth: cwidth,
      lineWidth: lwidth,
      scale: scale
    };
  };
  AbstractMathItem.prototype.state = function (state, restore) {
    if (state === void 0) {
      state = null;
    }
    if (restore === void 0) {
      restore = false;
    }
    if (state != null) {
      if (state < exports.STATE.INSERTED && this._state >= exports.STATE.INSERTED) {
        this.removeFromDocument(restore);
      }
      if (state < exports.STATE.TYPESET && this._state >= exports.STATE.TYPESET) {
        this.outputData = {};
      }
      if (state < exports.STATE.COMPILED && this._state >= exports.STATE.COMPILED) {
        this.inputData = {};
      }
      this._state = state;
    }
    return this._state;
  };
  AbstractMathItem.prototype.reset = function (restore) {
    if (restore === void 0) {
      restore = false;
    }
    this.state(exports.STATE.UNPROCESSED, restore);
  };
  return AbstractMathItem;
}();
exports.AbstractMathItem = AbstractMathItem;
exports.STATE = {
  UNPROCESSED: 0,
  FINDMATH: 10,
  COMPILED: 20,
  CONVERT: 100,
  METRICS: 110,
  RERENDER: 125,
  TYPESET: 150,
  INSERTED: 200,
  LAST: 10000
};
function newState(name, state) {
  if (name in exports.STATE) {
    throw Error('State ' + name + ' already exists');
  }
  exports.STATE[name] = state;
}
exports.newState = newState;

/***/ }),

/***/ 48790:
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
var __importDefault = this && this.__importDefault || function (mod) {
  return mod && mod.__esModule ? mod : {
    "default": mod
  };
};
Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports.TeX = void 0;
var InputJax_js_1 = __webpack_require__(87261);
var Options_js_1 = __webpack_require__(62704);
var FindTeX_js_1 = __webpack_require__(19666);
var FilterUtil_js_1 = __importDefault(__webpack_require__(86909));
var NodeUtil_js_1 = __importDefault(__webpack_require__(91085));
var TexParser_js_1 = __importDefault(__webpack_require__(19687));
var TexError_js_1 = __importDefault(__webpack_require__(19795));
var ParseOptions_js_1 = __importDefault(__webpack_require__(67252));
var Tags_js_1 = __webpack_require__(46041);
var Configuration_js_1 = __webpack_require__(34268);
__webpack_require__(55781);
var TeX = function (_super) {
  __extends(TeX, _super);
  function TeX(options) {
    if (options === void 0) {
      options = {};
    }
    var _this = this;
    var _a = __read((0, Options_js_1.separateOptions)(options, TeX.OPTIONS, FindTeX_js_1.FindTeX.OPTIONS), 3),
      rest = _a[0],
      tex = _a[1],
      find = _a[2];
    _this = _super.call(this, tex) || this;
    _this.findTeX = _this.options['FindTeX'] || new FindTeX_js_1.FindTeX(find);
    var packages = _this.options.packages;
    var configuration = _this.configuration = TeX.configure(packages);
    var parseOptions = _this._parseOptions = new ParseOptions_js_1.default(configuration, [_this.options, Tags_js_1.TagsFactory.OPTIONS]);
    (0, Options_js_1.userOptions)(parseOptions.options, rest);
    configuration.config(_this);
    TeX.tags(parseOptions, configuration);
    _this.postFilters.add(FilterUtil_js_1.default.cleanSubSup, -6);
    _this.postFilters.add(FilterUtil_js_1.default.setInherited, -5);
    _this.postFilters.add(FilterUtil_js_1.default.moveLimits, -4);
    _this.postFilters.add(FilterUtil_js_1.default.cleanStretchy, -3);
    _this.postFilters.add(FilterUtil_js_1.default.cleanAttributes, -2);
    _this.postFilters.add(FilterUtil_js_1.default.combineRelations, -1);
    return _this;
  }
  TeX.configure = function (packages) {
    var configuration = new Configuration_js_1.ParserConfiguration(packages, ['tex']);
    configuration.init();
    return configuration;
  };
  TeX.tags = function (options, configuration) {
    Tags_js_1.TagsFactory.addTags(configuration.tags);
    Tags_js_1.TagsFactory.setDefault(options.options.tags);
    options.tags = Tags_js_1.TagsFactory.getDefault();
    options.tags.configuration = options;
  };
  TeX.prototype.setMmlFactory = function (mmlFactory) {
    _super.prototype.setMmlFactory.call(this, mmlFactory);
    this._parseOptions.nodeFactory.setMmlFactory(mmlFactory);
  };
  Object.defineProperty(TeX.prototype, "parseOptions", {
    get: function () {
      return this._parseOptions;
    },
    enumerable: false,
    configurable: true
  });
  TeX.prototype.reset = function (tag) {
    if (tag === void 0) {
      tag = 0;
    }
    this.parseOptions.tags.reset(tag);
  };
  TeX.prototype.compile = function (math, document) {
    this.parseOptions.clear();
    this.executeFilters(this.preFilters, math, document, this.parseOptions);
    var display = math.display;
    this.latex = math.math;
    var node;
    this.parseOptions.tags.startEquation(math);
    var globalEnv;
    try {
      var parser = new TexParser_js_1.default(this.latex, {
        display: display,
        isInner: false
      }, this.parseOptions);
      node = parser.mml();
      globalEnv = parser.stack.global;
    } catch (err) {
      if (!(err instanceof TexError_js_1.default)) {
        throw err;
      }
      this.parseOptions.error = true;
      node = this.options.formatError(this, err);
    }
    node = this.parseOptions.nodeFactory.create('node', 'math', [node]);
    if (globalEnv === null || globalEnv === void 0 ? void 0 : globalEnv.indentalign) {
      NodeUtil_js_1.default.setAttribute(node, 'indentalign', globalEnv.indentalign);
    }
    if (display) {
      NodeUtil_js_1.default.setAttribute(node, 'display', 'block');
    }
    this.parseOptions.tags.finishEquation(math);
    this.parseOptions.root = node;
    this.executeFilters(this.postFilters, math, document, this.parseOptions);
    this.mathNode = this.parseOptions.root;
    return this.mathNode;
  };
  TeX.prototype.findMath = function (strings) {
    return this.findTeX.findMath(strings);
  };
  TeX.prototype.formatError = function (err) {
    var message = err.message.replace(/\n.*/, '');
    return this.parseOptions.nodeFactory.create('error', message, err.id, this.latex);
  };
  TeX.NAME = 'TeX';
  TeX.OPTIONS = __assign(__assign({}, InputJax_js_1.AbstractInputJax.OPTIONS), {
    FindTeX: null,
    packages: ['base'],
    digits: /^(?:[0-9]+(?:\{,\}[0-9]{3})*(?:\.[0-9]*)?|\.[0-9]+)/,
    maxBuffer: 5 * 1024,
    formatError: function (jax, err) {
      return jax.formatError(err);
    }
  });
  return TeX;
}(InputJax_js_1.AbstractInputJax);
exports.TeX = TeX;

/***/ }),

/***/ 86909:
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
var __importDefault = this && this.__importDefault || function (mod) {
  return mod && mod.__esModule ? mod : {
    "default": mod
  };
};
Object.defineProperty(exports, "__esModule", ({
  value: true
}));
var MmlNode_js_1 = __webpack_require__(34690);
var NodeUtil_js_1 = __importDefault(__webpack_require__(91085));
var FilterUtil;
(function (FilterUtil) {
  FilterUtil.cleanStretchy = function (arg) {
    var e_1, _a;
    var options = arg.data;
    try {
      for (var _b = __values(options.getList('fixStretchy')), _c = _b.next(); !_c.done; _c = _b.next()) {
        var mo = _c.value;
        if (NodeUtil_js_1.default.getProperty(mo, 'fixStretchy')) {
          var symbol = NodeUtil_js_1.default.getForm(mo);
          if (symbol && symbol[3] && symbol[3]['stretchy']) {
            NodeUtil_js_1.default.setAttribute(mo, 'stretchy', false);
          }
          var parent_1 = mo.parent;
          if (!NodeUtil_js_1.default.getTexClass(mo) && (!symbol || !symbol[2])) {
            var texAtom = options.nodeFactory.create('node', 'TeXAtom', [mo]);
            parent_1.replaceChild(texAtom, mo);
            texAtom.inheritAttributesFrom(mo);
          }
          NodeUtil_js_1.default.removeProperties(mo, 'fixStretchy');
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
  FilterUtil.cleanAttributes = function (arg) {
    var node = arg.data.root;
    node.walkTree(function (mml, _d) {
      var e_2, _a;
      var attribs = mml.attributes;
      if (!attribs) {
        return;
      }
      var keep = new Set((attribs.get('mjx-keep-attrs') || '').split(/ /));
      delete attribs.getAllAttributes()['mjx-keep-attrs'];
      try {
        for (var _b = __values(attribs.getExplicitNames()), _c = _b.next(); !_c.done; _c = _b.next()) {
          var key = _c.value;
          if (!keep.has(key) && attribs.attributes[key] === mml.attributes.getInherited(key)) {
            delete attribs.attributes[key];
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
    }, {});
  };
  FilterUtil.combineRelations = function (arg) {
    var e_3, _a, e_4, _b;
    var remove = [];
    try {
      for (var _c = __values(arg.data.getList('mo')), _e = _c.next(); !_e.done; _e = _c.next()) {
        var mo = _e.value;
        if (mo.getProperty('relationsCombined') || !mo.parent || mo.parent && !NodeUtil_js_1.default.isType(mo.parent, 'mrow') || NodeUtil_js_1.default.getTexClass(mo) !== MmlNode_js_1.TEXCLASS.REL) {
          continue;
        }
        var mml = mo.parent;
        var m2 = void 0;
        var children = mml.childNodes;
        var next = children.indexOf(mo) + 1;
        var variantForm = NodeUtil_js_1.default.getProperty(mo, 'variantForm');
        while (next < children.length && (m2 = children[next]) && NodeUtil_js_1.default.isType(m2, 'mo') && NodeUtil_js_1.default.getTexClass(m2) === MmlNode_js_1.TEXCLASS.REL) {
          if (variantForm === NodeUtil_js_1.default.getProperty(m2, 'variantForm') && _compareExplicit(mo, m2)) {
            NodeUtil_js_1.default.appendChildren(mo, NodeUtil_js_1.default.getChildren(m2));
            _copyExplicit(['stretchy', 'rspace'], mo, m2);
            try {
              for (var _f = (e_4 = void 0, __values(m2.getPropertyNames())), _g = _f.next(); !_g.done; _g = _f.next()) {
                var name_1 = _g.value;
                mo.setProperty(name_1, m2.getProperty(name_1));
              }
            } catch (e_4_1) {
              e_4 = {
                error: e_4_1
              };
            } finally {
              try {
                if (_g && !_g.done && (_b = _f.return)) _b.call(_f);
              } finally {
                if (e_4) throw e_4.error;
              }
            }
            children.splice(next, 1);
            remove.push(m2);
            m2.parent = null;
            m2.setProperty('relationsCombined', true);
          } else {
            if (mo.attributes.getExplicit('rspace') == null) {
              NodeUtil_js_1.default.setAttribute(mo, 'rspace', '0pt');
            }
            if (m2.attributes.getExplicit('lspace') == null) {
              NodeUtil_js_1.default.setAttribute(m2, 'lspace', '0pt');
            }
            break;
          }
        }
        mo.attributes.setInherited('form', mo.getForms()[0]);
      }
    } catch (e_3_1) {
      e_3 = {
        error: e_3_1
      };
    } finally {
      try {
        if (_e && !_e.done && (_a = _c.return)) _a.call(_c);
      } finally {
        if (e_3) throw e_3.error;
      }
    }
    arg.data.removeFromList('mo', remove);
  };
  var _copyExplicit = function (attrs, node1, node2) {
    var attr1 = node1.attributes;
    var attr2 = node2.attributes;
    attrs.forEach(function (x) {
      var attr = attr2.getExplicit(x);
      if (attr != null) {
        attr1.set(x, attr);
      }
    });
  };
  var _compareExplicit = function (node1, node2) {
    var e_5, _a;
    var filter = function (attr, space) {
      var exp = attr.getExplicitNames();
      return exp.filter(function (x) {
        return x !== space && (x !== 'stretchy' || attr.getExplicit('stretchy'));
      });
    };
    var attr1 = node1.attributes;
    var attr2 = node2.attributes;
    var exp1 = filter(attr1, 'lspace');
    var exp2 = filter(attr2, 'rspace');
    if (exp1.length !== exp2.length) {
      return false;
    }
    try {
      for (var exp1_1 = __values(exp1), exp1_1_1 = exp1_1.next(); !exp1_1_1.done; exp1_1_1 = exp1_1.next()) {
        var name_2 = exp1_1_1.value;
        if (attr1.getExplicit(name_2) !== attr2.getExplicit(name_2)) {
          return false;
        }
      }
    } catch (e_5_1) {
      e_5 = {
        error: e_5_1
      };
    } finally {
      try {
        if (exp1_1_1 && !exp1_1_1.done && (_a = exp1_1.return)) _a.call(exp1_1);
      } finally {
        if (e_5) throw e_5.error;
      }
    }
    return true;
  };
  var _cleanSubSup = function (options, low, up) {
    var e_6, _a;
    var remove = [];
    try {
      for (var _b = __values(options.getList('m' + low + up)), _c = _b.next(); !_c.done; _c = _b.next()) {
        var mml = _c.value;
        var children = mml.childNodes;
        if (children[mml[low]] && children[mml[up]]) {
          continue;
        }
        var parent_2 = mml.parent;
        var newNode = children[mml[low]] ? options.nodeFactory.create('node', 'm' + low, [children[mml.base], children[mml[low]]]) : options.nodeFactory.create('node', 'm' + up, [children[mml.base], children[mml[up]]]);
        NodeUtil_js_1.default.copyAttributes(mml, newNode);
        if (parent_2) {
          parent_2.replaceChild(newNode, mml);
        } else {
          options.root = newNode;
        }
        remove.push(mml);
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
    options.removeFromList('m' + low + up, remove);
  };
  FilterUtil.cleanSubSup = function (arg) {
    var options = arg.data;
    if (options.error) {
      return;
    }
    _cleanSubSup(options, 'sub', 'sup');
    _cleanSubSup(options, 'under', 'over');
  };
  var _moveLimits = function (options, underover, subsup) {
    var e_7, _a;
    var remove = [];
    try {
      for (var _b = __values(options.getList(underover)), _c = _b.next(); !_c.done; _c = _b.next()) {
        var mml = _c.value;
        if (mml.attributes.get('displaystyle')) {
          continue;
        }
        var base = mml.childNodes[mml.base];
        var mo = base.coreMO();
        if (base.getProperty('movablelimits') && !mo.attributes.getExplicit('movablelimits')) {
          var node = options.nodeFactory.create('node', subsup, mml.childNodes);
          NodeUtil_js_1.default.copyAttributes(mml, node);
          if (mml.parent) {
            mml.parent.replaceChild(node, mml);
          } else {
            options.root = node;
          }
          remove.push(mml);
        }
      }
    } catch (e_7_1) {
      e_7 = {
        error: e_7_1
      };
    } finally {
      try {
        if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
      } finally {
        if (e_7) throw e_7.error;
      }
    }
    options.removeFromList(underover, remove);
  };
  FilterUtil.moveLimits = function (arg) {
    var options = arg.data;
    _moveLimits(options, 'munderover', 'msubsup');
    _moveLimits(options, 'munder', 'msub');
    _moveLimits(options, 'mover', 'msup');
  };
  FilterUtil.setInherited = function (arg) {
    arg.data.root.setInheritedAttributes({}, arg.math['display'], 0, false);
  };
})(FilterUtil || (FilterUtil = {}));
exports["default"] = FilterUtil;

/***/ }),

/***/ 19666:
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
exports.FindTeX = void 0;
var FindMath_js_1 = __webpack_require__(72177);
var string_js_1 = __webpack_require__(23912);
var MathItem_js_1 = __webpack_require__(57714);
var FindTeX = function (_super) {
  __extends(FindTeX, _super);
  function FindTeX(options) {
    var _this = _super.call(this, options) || this;
    _this.getPatterns();
    return _this;
  }
  FindTeX.prototype.getPatterns = function () {
    var _this = this;
    var options = this.options;
    var starts = [],
      parts = [],
      subparts = [];
    this.end = {};
    this.env = this.sub = 0;
    var i = 1;
    options['inlineMath'].forEach(function (delims) {
      return _this.addPattern(starts, delims, false);
    });
    options['displayMath'].forEach(function (delims) {
      return _this.addPattern(starts, delims, true);
    });
    if (starts.length) {
      parts.push(starts.sort(string_js_1.sortLength).join('|'));
    }
    if (options['processEnvironments']) {
      parts.push('\\\\begin\\s*\\{([^}]*)\\}');
      this.env = i;
      i++;
    }
    if (options['processEscapes']) {
      subparts.push('\\\\([\\\\$])');
    }
    if (options['processRefs']) {
      subparts.push('(\\\\(?:eq)?ref\\s*\\{[^}]*\\})');
    }
    if (subparts.length) {
      parts.push('(' + subparts.join('|') + ')');
      this.sub = i;
    }
    this.start = new RegExp(parts.join('|'), 'g');
    this.hasPatterns = parts.length > 0;
  };
  FindTeX.prototype.addPattern = function (starts, delims, display) {
    var _a = __read(delims, 2),
      open = _a[0],
      close = _a[1];
    starts.push((0, string_js_1.quotePattern)(open));
    this.end[open] = [close, display, this.endPattern(close)];
  };
  FindTeX.prototype.endPattern = function (end, endp) {
    return new RegExp((endp || (0, string_js_1.quotePattern)(end)) + '|\\\\(?:[a-zA-Z]|.)|[{}]', 'g');
  };
  FindTeX.prototype.findEnd = function (text, n, start, end) {
    var _a = __read(end, 3),
      close = _a[0],
      display = _a[1],
      pattern = _a[2];
    var i = pattern.lastIndex = start.index + start[0].length;
    var match,
      braces = 0;
    while (match = pattern.exec(text)) {
      if ((match[1] || match[0]) === close && braces === 0) {
        return (0, MathItem_js_1.protoItem)(start[0], text.substr(i, match.index - i), match[0], n, start.index, match.index + match[0].length, display);
      } else if (match[0] === '{') {
        braces++;
      } else if (match[0] === '}' && braces) {
        braces--;
      }
    }
    return null;
  };
  FindTeX.prototype.findMathInString = function (math, n, text) {
    var start, match;
    this.start.lastIndex = 0;
    while (start = this.start.exec(text)) {
      if (start[this.env] !== undefined && this.env) {
        var end = '\\\\end\\s*(\\{' + (0, string_js_1.quotePattern)(start[this.env]) + '\\})';
        match = this.findEnd(text, n, start, ['{' + start[this.env] + '}', true, this.endPattern(null, end)]);
        if (match) {
          match.math = match.open + match.math + match.close;
          match.open = match.close = '';
        }
      } else if (start[this.sub] !== undefined && this.sub) {
        var math_1 = start[this.sub];
        var end = start.index + start[this.sub].length;
        if (math_1.length === 2) {
          match = (0, MathItem_js_1.protoItem)('', math_1.substr(1), '', n, start.index, end);
        } else {
          match = (0, MathItem_js_1.protoItem)('', math_1, '', n, start.index, end, false);
        }
      } else {
        match = this.findEnd(text, n, start, this.end[start[0]]);
      }
      if (match) {
        math.push(match);
        this.start.lastIndex = match.end.n;
      }
    }
  };
  FindTeX.prototype.findMath = function (strings) {
    var math = [];
    if (this.hasPatterns) {
      for (var i = 0, m = strings.length; i < m; i++) {
        this.findMathInString(math, i, strings[i]);
      }
    }
    return math;
  };
  FindTeX.OPTIONS = {
    inlineMath: [['\\(', '\\)']],
    displayMath: [['$$', '$$'], ['\\[', '\\]']],
    processEscapes: true,
    processEnvironments: true,
    processRefs: true
  };
  return FindTeX;
}(FindMath_js_1.AbstractFindMath);
exports.FindTeX = FindTeX;

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiODc5MC5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7QUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7Ozs7OztBQ2ZBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOzs7Ozs7O0FDL0RBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7Ozs7OztBQ2pLQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7Ozs7OztBQ3ZMQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOzs7Ozs7O0FDOVJBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AZGF0YWxheWVyL2p1cHl0ZXItdmlld2VyLy4vbm9kZV9tb2R1bGVzL21hdGhqYXgtZnVsbC9qcy9jb3JlL0ZpbmRNYXRoLmpzIiwid2VicGFjazovL0BkYXRhbGF5ZXIvanVweXRlci12aWV3ZXIvLi9ub2RlX21vZHVsZXMvbWF0aGpheC1mdWxsL2pzL2NvcmUvSW5wdXRKYXguanMiLCJ3ZWJwYWNrOi8vQGRhdGFsYXllci9qdXB5dGVyLXZpZXdlci8uL25vZGVfbW9kdWxlcy9tYXRoamF4LWZ1bGwvanMvY29yZS9NYXRoSXRlbS5qcyIsIndlYnBhY2s6Ly9AZGF0YWxheWVyL2p1cHl0ZXItdmlld2VyLy4vbm9kZV9tb2R1bGVzL21hdGhqYXgtZnVsbC9qcy9pbnB1dC90ZXguanMiLCJ3ZWJwYWNrOi8vQGRhdGFsYXllci9qdXB5dGVyLXZpZXdlci8uL25vZGVfbW9kdWxlcy9tYXRoamF4LWZ1bGwvanMvaW5wdXQvdGV4L0ZpbHRlclV0aWwuanMiLCJ3ZWJwYWNrOi8vQGRhdGFsYXllci9qdXB5dGVyLXZpZXdlci8uL25vZGVfbW9kdWxlcy9tYXRoamF4LWZ1bGwvanMvaW5wdXQvdGV4L0ZpbmRUZVguanMiXSwic291cmNlc0NvbnRlbnQiOlsiXCJ1c2Ugc3RyaWN0XCI7XG5cbk9iamVjdC5kZWZpbmVQcm9wZXJ0eShleHBvcnRzLCBcIl9fZXNNb2R1bGVcIiwge1xuICB2YWx1ZTogdHJ1ZVxufSk7XG5leHBvcnRzLkFic3RyYWN0RmluZE1hdGggPSB2b2lkIDA7XG52YXIgT3B0aW9uc19qc18xID0gcmVxdWlyZShcIi4uL3V0aWwvT3B0aW9ucy5qc1wiKTtcbnZhciBBYnN0cmFjdEZpbmRNYXRoID0gZnVuY3Rpb24gKCkge1xuICBmdW5jdGlvbiBBYnN0cmFjdEZpbmRNYXRoKG9wdGlvbnMpIHtcbiAgICB2YXIgQ0xBU1MgPSB0aGlzLmNvbnN0cnVjdG9yO1xuICAgIHRoaXMub3B0aW9ucyA9ICgwLCBPcHRpb25zX2pzXzEudXNlck9wdGlvbnMpKCgwLCBPcHRpb25zX2pzXzEuZGVmYXVsdE9wdGlvbnMpKHt9LCBDTEFTUy5PUFRJT05TKSwgb3B0aW9ucyk7XG4gIH1cbiAgQWJzdHJhY3RGaW5kTWF0aC5PUFRJT05TID0ge307XG4gIHJldHVybiBBYnN0cmFjdEZpbmRNYXRoO1xufSgpO1xuZXhwb3J0cy5BYnN0cmFjdEZpbmRNYXRoID0gQWJzdHJhY3RGaW5kTWF0aDsiLCJcInVzZSBzdHJpY3RcIjtcblxuT2JqZWN0LmRlZmluZVByb3BlcnR5KGV4cG9ydHMsIFwiX19lc01vZHVsZVwiLCB7XG4gIHZhbHVlOiB0cnVlXG59KTtcbmV4cG9ydHMuQWJzdHJhY3RJbnB1dEpheCA9IHZvaWQgMDtcbnZhciBPcHRpb25zX2pzXzEgPSByZXF1aXJlKFwiLi4vdXRpbC9PcHRpb25zLmpzXCIpO1xudmFyIEZ1bmN0aW9uTGlzdF9qc18xID0gcmVxdWlyZShcIi4uL3V0aWwvRnVuY3Rpb25MaXN0LmpzXCIpO1xudmFyIEFic3RyYWN0SW5wdXRKYXggPSBmdW5jdGlvbiAoKSB7XG4gIGZ1bmN0aW9uIEFic3RyYWN0SW5wdXRKYXgob3B0aW9ucykge1xuICAgIGlmIChvcHRpb25zID09PSB2b2lkIDApIHtcbiAgICAgIG9wdGlvbnMgPSB7fTtcbiAgICB9XG4gICAgdGhpcy5hZGFwdG9yID0gbnVsbDtcbiAgICB0aGlzLm1tbEZhY3RvcnkgPSBudWxsO1xuICAgIHZhciBDTEFTUyA9IHRoaXMuY29uc3RydWN0b3I7XG4gICAgdGhpcy5vcHRpb25zID0gKDAsIE9wdGlvbnNfanNfMS51c2VyT3B0aW9ucykoKDAsIE9wdGlvbnNfanNfMS5kZWZhdWx0T3B0aW9ucykoe30sIENMQVNTLk9QVElPTlMpLCBvcHRpb25zKTtcbiAgICB0aGlzLnByZUZpbHRlcnMgPSBuZXcgRnVuY3Rpb25MaXN0X2pzXzEuRnVuY3Rpb25MaXN0KCk7XG4gICAgdGhpcy5wb3N0RmlsdGVycyA9IG5ldyBGdW5jdGlvbkxpc3RfanNfMS5GdW5jdGlvbkxpc3QoKTtcbiAgfVxuICBPYmplY3QuZGVmaW5lUHJvcGVydHkoQWJzdHJhY3RJbnB1dEpheC5wcm90b3R5cGUsIFwibmFtZVwiLCB7XG4gICAgZ2V0OiBmdW5jdGlvbiAoKSB7XG4gICAgICByZXR1cm4gdGhpcy5jb25zdHJ1Y3Rvci5OQU1FO1xuICAgIH0sXG4gICAgZW51bWVyYWJsZTogZmFsc2UsXG4gICAgY29uZmlndXJhYmxlOiB0cnVlXG4gIH0pO1xuICBBYnN0cmFjdElucHV0SmF4LnByb3RvdHlwZS5zZXRBZGFwdG9yID0gZnVuY3Rpb24gKGFkYXB0b3IpIHtcbiAgICB0aGlzLmFkYXB0b3IgPSBhZGFwdG9yO1xuICB9O1xuICBBYnN0cmFjdElucHV0SmF4LnByb3RvdHlwZS5zZXRNbWxGYWN0b3J5ID0gZnVuY3Rpb24gKG1tbEZhY3RvcnkpIHtcbiAgICB0aGlzLm1tbEZhY3RvcnkgPSBtbWxGYWN0b3J5O1xuICB9O1xuICBBYnN0cmFjdElucHV0SmF4LnByb3RvdHlwZS5pbml0aWFsaXplID0gZnVuY3Rpb24gKCkge307XG4gIEFic3RyYWN0SW5wdXRKYXgucHJvdG90eXBlLnJlc2V0ID0gZnVuY3Rpb24gKCkge1xuICAgIHZhciBfYXJncyA9IFtdO1xuICAgIGZvciAodmFyIF9pID0gMDsgX2kgPCBhcmd1bWVudHMubGVuZ3RoOyBfaSsrKSB7XG4gICAgICBfYXJnc1tfaV0gPSBhcmd1bWVudHNbX2ldO1xuICAgIH1cbiAgfTtcbiAgT2JqZWN0LmRlZmluZVByb3BlcnR5KEFic3RyYWN0SW5wdXRKYXgucHJvdG90eXBlLCBcInByb2Nlc3NTdHJpbmdzXCIsIHtcbiAgICBnZXQ6IGZ1bmN0aW9uICgpIHtcbiAgICAgIHJldHVybiB0cnVlO1xuICAgIH0sXG4gICAgZW51bWVyYWJsZTogZmFsc2UsXG4gICAgY29uZmlndXJhYmxlOiB0cnVlXG4gIH0pO1xuICBBYnN0cmFjdElucHV0SmF4LnByb3RvdHlwZS5maW5kTWF0aCA9IGZ1bmN0aW9uIChfbm9kZSwgX29wdGlvbnMpIHtcbiAgICByZXR1cm4gW107XG4gIH07XG4gIEFic3RyYWN0SW5wdXRKYXgucHJvdG90eXBlLmV4ZWN1dGVGaWx0ZXJzID0gZnVuY3Rpb24gKGZpbHRlcnMsIG1hdGgsIGRvY3VtZW50LCBkYXRhKSB7XG4gICAgdmFyIGFyZ3MgPSB7XG4gICAgICBtYXRoOiBtYXRoLFxuICAgICAgZG9jdW1lbnQ6IGRvY3VtZW50LFxuICAgICAgZGF0YTogZGF0YVxuICAgIH07XG4gICAgZmlsdGVycy5leGVjdXRlKGFyZ3MpO1xuICAgIHJldHVybiBhcmdzLmRhdGE7XG4gIH07XG4gIEFic3RyYWN0SW5wdXRKYXguTkFNRSA9ICdnZW5lcmljJztcbiAgQWJzdHJhY3RJbnB1dEpheC5PUFRJT05TID0ge307XG4gIHJldHVybiBBYnN0cmFjdElucHV0SmF4O1xufSgpO1xuZXhwb3J0cy5BYnN0cmFjdElucHV0SmF4ID0gQWJzdHJhY3RJbnB1dEpheDsiLCJcInVzZSBzdHJpY3RcIjtcblxuT2JqZWN0LmRlZmluZVByb3BlcnR5KGV4cG9ydHMsIFwiX19lc01vZHVsZVwiLCB7XG4gIHZhbHVlOiB0cnVlXG59KTtcbmV4cG9ydHMubmV3U3RhdGUgPSBleHBvcnRzLlNUQVRFID0gZXhwb3J0cy5BYnN0cmFjdE1hdGhJdGVtID0gZXhwb3J0cy5wcm90b0l0ZW0gPSB2b2lkIDA7XG5mdW5jdGlvbiBwcm90b0l0ZW0ob3BlbiwgbWF0aCwgY2xvc2UsIG4sIHN0YXJ0LCBlbmQsIGRpc3BsYXkpIHtcbiAgaWYgKGRpc3BsYXkgPT09IHZvaWQgMCkge1xuICAgIGRpc3BsYXkgPSBudWxsO1xuICB9XG4gIHZhciBpdGVtID0ge1xuICAgIG9wZW46IG9wZW4sXG4gICAgbWF0aDogbWF0aCxcbiAgICBjbG9zZTogY2xvc2UsXG4gICAgbjogbixcbiAgICBzdGFydDoge1xuICAgICAgbjogc3RhcnRcbiAgICB9LFxuICAgIGVuZDoge1xuICAgICAgbjogZW5kXG4gICAgfSxcbiAgICBkaXNwbGF5OiBkaXNwbGF5XG4gIH07XG4gIHJldHVybiBpdGVtO1xufVxuZXhwb3J0cy5wcm90b0l0ZW0gPSBwcm90b0l0ZW07XG52YXIgQWJzdHJhY3RNYXRoSXRlbSA9IGZ1bmN0aW9uICgpIHtcbiAgZnVuY3Rpb24gQWJzdHJhY3RNYXRoSXRlbShtYXRoLCBqYXgsIGRpc3BsYXksIHN0YXJ0LCBlbmQpIHtcbiAgICBpZiAoZGlzcGxheSA9PT0gdm9pZCAwKSB7XG4gICAgICBkaXNwbGF5ID0gdHJ1ZTtcbiAgICB9XG4gICAgaWYgKHN0YXJ0ID09PSB2b2lkIDApIHtcbiAgICAgIHN0YXJ0ID0ge1xuICAgICAgICBpOiAwLFxuICAgICAgICBuOiAwLFxuICAgICAgICBkZWxpbTogJydcbiAgICAgIH07XG4gICAgfVxuICAgIGlmIChlbmQgPT09IHZvaWQgMCkge1xuICAgICAgZW5kID0ge1xuICAgICAgICBpOiAwLFxuICAgICAgICBuOiAwLFxuICAgICAgICBkZWxpbTogJydcbiAgICAgIH07XG4gICAgfVxuICAgIHRoaXMucm9vdCA9IG51bGw7XG4gICAgdGhpcy50eXBlc2V0Um9vdCA9IG51bGw7XG4gICAgdGhpcy5tZXRyaWNzID0ge307XG4gICAgdGhpcy5pbnB1dERhdGEgPSB7fTtcbiAgICB0aGlzLm91dHB1dERhdGEgPSB7fTtcbiAgICB0aGlzLl9zdGF0ZSA9IGV4cG9ydHMuU1RBVEUuVU5QUk9DRVNTRUQ7XG4gICAgdGhpcy5tYXRoID0gbWF0aDtcbiAgICB0aGlzLmlucHV0SmF4ID0gamF4O1xuICAgIHRoaXMuZGlzcGxheSA9IGRpc3BsYXk7XG4gICAgdGhpcy5zdGFydCA9IHN0YXJ0O1xuICAgIHRoaXMuZW5kID0gZW5kO1xuICAgIHRoaXMucm9vdCA9IG51bGw7XG4gICAgdGhpcy50eXBlc2V0Um9vdCA9IG51bGw7XG4gICAgdGhpcy5tZXRyaWNzID0ge307XG4gICAgdGhpcy5pbnB1dERhdGEgPSB7fTtcbiAgICB0aGlzLm91dHB1dERhdGEgPSB7fTtcbiAgfVxuICBPYmplY3QuZGVmaW5lUHJvcGVydHkoQWJzdHJhY3RNYXRoSXRlbS5wcm90b3R5cGUsIFwiaXNFc2NhcGVkXCIsIHtcbiAgICBnZXQ6IGZ1bmN0aW9uICgpIHtcbiAgICAgIHJldHVybiB0aGlzLmRpc3BsYXkgPT09IG51bGw7XG4gICAgfSxcbiAgICBlbnVtZXJhYmxlOiBmYWxzZSxcbiAgICBjb25maWd1cmFibGU6IHRydWVcbiAgfSk7XG4gIEFic3RyYWN0TWF0aEl0ZW0ucHJvdG90eXBlLnJlbmRlciA9IGZ1bmN0aW9uIChkb2N1bWVudCkge1xuICAgIGRvY3VtZW50LnJlbmRlckFjdGlvbnMucmVuZGVyTWF0aCh0aGlzLCBkb2N1bWVudCk7XG4gIH07XG4gIEFic3RyYWN0TWF0aEl0ZW0ucHJvdG90eXBlLnJlcmVuZGVyID0gZnVuY3Rpb24gKGRvY3VtZW50LCBzdGFydCkge1xuICAgIGlmIChzdGFydCA9PT0gdm9pZCAwKSB7XG4gICAgICBzdGFydCA9IGV4cG9ydHMuU1RBVEUuUkVSRU5ERVI7XG4gICAgfVxuICAgIGlmICh0aGlzLnN0YXRlKCkgPj0gc3RhcnQpIHtcbiAgICAgIHRoaXMuc3RhdGUoc3RhcnQgLSAxKTtcbiAgICB9XG4gICAgZG9jdW1lbnQucmVuZGVyQWN0aW9ucy5yZW5kZXJNYXRoKHRoaXMsIGRvY3VtZW50LCBzdGFydCk7XG4gIH07XG4gIEFic3RyYWN0TWF0aEl0ZW0ucHJvdG90eXBlLmNvbnZlcnQgPSBmdW5jdGlvbiAoZG9jdW1lbnQsIGVuZCkge1xuICAgIGlmIChlbmQgPT09IHZvaWQgMCkge1xuICAgICAgZW5kID0gZXhwb3J0cy5TVEFURS5MQVNUO1xuICAgIH1cbiAgICBkb2N1bWVudC5yZW5kZXJBY3Rpb25zLnJlbmRlckNvbnZlcnQodGhpcywgZG9jdW1lbnQsIGVuZCk7XG4gIH07XG4gIEFic3RyYWN0TWF0aEl0ZW0ucHJvdG90eXBlLmNvbXBpbGUgPSBmdW5jdGlvbiAoZG9jdW1lbnQpIHtcbiAgICBpZiAodGhpcy5zdGF0ZSgpIDwgZXhwb3J0cy5TVEFURS5DT01QSUxFRCkge1xuICAgICAgdGhpcy5yb290ID0gdGhpcy5pbnB1dEpheC5jb21waWxlKHRoaXMsIGRvY3VtZW50KTtcbiAgICAgIHRoaXMuc3RhdGUoZXhwb3J0cy5TVEFURS5DT01QSUxFRCk7XG4gICAgfVxuICB9O1xuICBBYnN0cmFjdE1hdGhJdGVtLnByb3RvdHlwZS50eXBlc2V0ID0gZnVuY3Rpb24gKGRvY3VtZW50KSB7XG4gICAgaWYgKHRoaXMuc3RhdGUoKSA8IGV4cG9ydHMuU1RBVEUuVFlQRVNFVCkge1xuICAgICAgdGhpcy50eXBlc2V0Um9vdCA9IGRvY3VtZW50Lm91dHB1dEpheFt0aGlzLmlzRXNjYXBlZCA/ICdlc2NhcGVkJyA6ICd0eXBlc2V0J10odGhpcywgZG9jdW1lbnQpO1xuICAgICAgdGhpcy5zdGF0ZShleHBvcnRzLlNUQVRFLlRZUEVTRVQpO1xuICAgIH1cbiAgfTtcbiAgQWJzdHJhY3RNYXRoSXRlbS5wcm90b3R5cGUudXBkYXRlRG9jdW1lbnQgPSBmdW5jdGlvbiAoX2RvY3VtZW50KSB7fTtcbiAgQWJzdHJhY3RNYXRoSXRlbS5wcm90b3R5cGUucmVtb3ZlRnJvbURvY3VtZW50ID0gZnVuY3Rpb24gKF9yZXN0b3JlKSB7XG4gICAgaWYgKF9yZXN0b3JlID09PSB2b2lkIDApIHtcbiAgICAgIF9yZXN0b3JlID0gZmFsc2U7XG4gICAgfVxuICB9O1xuICBBYnN0cmFjdE1hdGhJdGVtLnByb3RvdHlwZS5zZXRNZXRyaWNzID0gZnVuY3Rpb24gKGVtLCBleCwgY3dpZHRoLCBsd2lkdGgsIHNjYWxlKSB7XG4gICAgdGhpcy5tZXRyaWNzID0ge1xuICAgICAgZW06IGVtLFxuICAgICAgZXg6IGV4LFxuICAgICAgY29udGFpbmVyV2lkdGg6IGN3aWR0aCxcbiAgICAgIGxpbmVXaWR0aDogbHdpZHRoLFxuICAgICAgc2NhbGU6IHNjYWxlXG4gICAgfTtcbiAgfTtcbiAgQWJzdHJhY3RNYXRoSXRlbS5wcm90b3R5cGUuc3RhdGUgPSBmdW5jdGlvbiAoc3RhdGUsIHJlc3RvcmUpIHtcbiAgICBpZiAoc3RhdGUgPT09IHZvaWQgMCkge1xuICAgICAgc3RhdGUgPSBudWxsO1xuICAgIH1cbiAgICBpZiAocmVzdG9yZSA9PT0gdm9pZCAwKSB7XG4gICAgICByZXN0b3JlID0gZmFsc2U7XG4gICAgfVxuICAgIGlmIChzdGF0ZSAhPSBudWxsKSB7XG4gICAgICBpZiAoc3RhdGUgPCBleHBvcnRzLlNUQVRFLklOU0VSVEVEICYmIHRoaXMuX3N0YXRlID49IGV4cG9ydHMuU1RBVEUuSU5TRVJURUQpIHtcbiAgICAgICAgdGhpcy5yZW1vdmVGcm9tRG9jdW1lbnQocmVzdG9yZSk7XG4gICAgICB9XG4gICAgICBpZiAoc3RhdGUgPCBleHBvcnRzLlNUQVRFLlRZUEVTRVQgJiYgdGhpcy5fc3RhdGUgPj0gZXhwb3J0cy5TVEFURS5UWVBFU0VUKSB7XG4gICAgICAgIHRoaXMub3V0cHV0RGF0YSA9IHt9O1xuICAgICAgfVxuICAgICAgaWYgKHN0YXRlIDwgZXhwb3J0cy5TVEFURS5DT01QSUxFRCAmJiB0aGlzLl9zdGF0ZSA+PSBleHBvcnRzLlNUQVRFLkNPTVBJTEVEKSB7XG4gICAgICAgIHRoaXMuaW5wdXREYXRhID0ge307XG4gICAgICB9XG4gICAgICB0aGlzLl9zdGF0ZSA9IHN0YXRlO1xuICAgIH1cbiAgICByZXR1cm4gdGhpcy5fc3RhdGU7XG4gIH07XG4gIEFic3RyYWN0TWF0aEl0ZW0ucHJvdG90eXBlLnJlc2V0ID0gZnVuY3Rpb24gKHJlc3RvcmUpIHtcbiAgICBpZiAocmVzdG9yZSA9PT0gdm9pZCAwKSB7XG4gICAgICByZXN0b3JlID0gZmFsc2U7XG4gICAgfVxuICAgIHRoaXMuc3RhdGUoZXhwb3J0cy5TVEFURS5VTlBST0NFU1NFRCwgcmVzdG9yZSk7XG4gIH07XG4gIHJldHVybiBBYnN0cmFjdE1hdGhJdGVtO1xufSgpO1xuZXhwb3J0cy5BYnN0cmFjdE1hdGhJdGVtID0gQWJzdHJhY3RNYXRoSXRlbTtcbmV4cG9ydHMuU1RBVEUgPSB7XG4gIFVOUFJPQ0VTU0VEOiAwLFxuICBGSU5ETUFUSDogMTAsXG4gIENPTVBJTEVEOiAyMCxcbiAgQ09OVkVSVDogMTAwLFxuICBNRVRSSUNTOiAxMTAsXG4gIFJFUkVOREVSOiAxMjUsXG4gIFRZUEVTRVQ6IDE1MCxcbiAgSU5TRVJURUQ6IDIwMCxcbiAgTEFTVDogMTAwMDBcbn07XG5mdW5jdGlvbiBuZXdTdGF0ZShuYW1lLCBzdGF0ZSkge1xuICBpZiAobmFtZSBpbiBleHBvcnRzLlNUQVRFKSB7XG4gICAgdGhyb3cgRXJyb3IoJ1N0YXRlICcgKyBuYW1lICsgJyBhbHJlYWR5IGV4aXN0cycpO1xuICB9XG4gIGV4cG9ydHMuU1RBVEVbbmFtZV0gPSBzdGF0ZTtcbn1cbmV4cG9ydHMubmV3U3RhdGUgPSBuZXdTdGF0ZTsiLCJcInVzZSBzdHJpY3RcIjtcblxudmFyIF9fZXh0ZW5kcyA9IHRoaXMgJiYgdGhpcy5fX2V4dGVuZHMgfHwgZnVuY3Rpb24gKCkge1xuICB2YXIgZXh0ZW5kU3RhdGljcyA9IGZ1bmN0aW9uIChkLCBiKSB7XG4gICAgZXh0ZW5kU3RhdGljcyA9IE9iamVjdC5zZXRQcm90b3R5cGVPZiB8fCB7XG4gICAgICBfX3Byb3RvX186IFtdXG4gICAgfSBpbnN0YW5jZW9mIEFycmF5ICYmIGZ1bmN0aW9uIChkLCBiKSB7XG4gICAgICBkLl9fcHJvdG9fXyA9IGI7XG4gICAgfSB8fCBmdW5jdGlvbiAoZCwgYikge1xuICAgICAgZm9yICh2YXIgcCBpbiBiKSBpZiAoT2JqZWN0LnByb3RvdHlwZS5oYXNPd25Qcm9wZXJ0eS5jYWxsKGIsIHApKSBkW3BdID0gYltwXTtcbiAgICB9O1xuICAgIHJldHVybiBleHRlbmRTdGF0aWNzKGQsIGIpO1xuICB9O1xuICByZXR1cm4gZnVuY3Rpb24gKGQsIGIpIHtcbiAgICBpZiAodHlwZW9mIGIgIT09IFwiZnVuY3Rpb25cIiAmJiBiICE9PSBudWxsKSB0aHJvdyBuZXcgVHlwZUVycm9yKFwiQ2xhc3MgZXh0ZW5kcyB2YWx1ZSBcIiArIFN0cmluZyhiKSArIFwiIGlzIG5vdCBhIGNvbnN0cnVjdG9yIG9yIG51bGxcIik7XG4gICAgZXh0ZW5kU3RhdGljcyhkLCBiKTtcbiAgICBmdW5jdGlvbiBfXygpIHtcbiAgICAgIHRoaXMuY29uc3RydWN0b3IgPSBkO1xuICAgIH1cbiAgICBkLnByb3RvdHlwZSA9IGIgPT09IG51bGwgPyBPYmplY3QuY3JlYXRlKGIpIDogKF9fLnByb3RvdHlwZSA9IGIucHJvdG90eXBlLCBuZXcgX18oKSk7XG4gIH07XG59KCk7XG52YXIgX19hc3NpZ24gPSB0aGlzICYmIHRoaXMuX19hc3NpZ24gfHwgZnVuY3Rpb24gKCkge1xuICBfX2Fzc2lnbiA9IE9iamVjdC5hc3NpZ24gfHwgZnVuY3Rpb24gKHQpIHtcbiAgICBmb3IgKHZhciBzLCBpID0gMSwgbiA9IGFyZ3VtZW50cy5sZW5ndGg7IGkgPCBuOyBpKyspIHtcbiAgICAgIHMgPSBhcmd1bWVudHNbaV07XG4gICAgICBmb3IgKHZhciBwIGluIHMpIGlmIChPYmplY3QucHJvdG90eXBlLmhhc093blByb3BlcnR5LmNhbGwocywgcCkpIHRbcF0gPSBzW3BdO1xuICAgIH1cbiAgICByZXR1cm4gdDtcbiAgfTtcbiAgcmV0dXJuIF9fYXNzaWduLmFwcGx5KHRoaXMsIGFyZ3VtZW50cyk7XG59O1xudmFyIF9fcmVhZCA9IHRoaXMgJiYgdGhpcy5fX3JlYWQgfHwgZnVuY3Rpb24gKG8sIG4pIHtcbiAgdmFyIG0gPSB0eXBlb2YgU3ltYm9sID09PSBcImZ1bmN0aW9uXCIgJiYgb1tTeW1ib2wuaXRlcmF0b3JdO1xuICBpZiAoIW0pIHJldHVybiBvO1xuICB2YXIgaSA9IG0uY2FsbChvKSxcbiAgICByLFxuICAgIGFyID0gW10sXG4gICAgZTtcbiAgdHJ5IHtcbiAgICB3aGlsZSAoKG4gPT09IHZvaWQgMCB8fCBuLS0gPiAwKSAmJiAhKHIgPSBpLm5leHQoKSkuZG9uZSkgYXIucHVzaChyLnZhbHVlKTtcbiAgfSBjYXRjaCAoZXJyb3IpIHtcbiAgICBlID0ge1xuICAgICAgZXJyb3I6IGVycm9yXG4gICAgfTtcbiAgfSBmaW5hbGx5IHtcbiAgICB0cnkge1xuICAgICAgaWYgKHIgJiYgIXIuZG9uZSAmJiAobSA9IGlbXCJyZXR1cm5cIl0pKSBtLmNhbGwoaSk7XG4gICAgfSBmaW5hbGx5IHtcbiAgICAgIGlmIChlKSB0aHJvdyBlLmVycm9yO1xuICAgIH1cbiAgfVxuICByZXR1cm4gYXI7XG59O1xudmFyIF9faW1wb3J0RGVmYXVsdCA9IHRoaXMgJiYgdGhpcy5fX2ltcG9ydERlZmF1bHQgfHwgZnVuY3Rpb24gKG1vZCkge1xuICByZXR1cm4gbW9kICYmIG1vZC5fX2VzTW9kdWxlID8gbW9kIDoge1xuICAgIFwiZGVmYXVsdFwiOiBtb2RcbiAgfTtcbn07XG5PYmplY3QuZGVmaW5lUHJvcGVydHkoZXhwb3J0cywgXCJfX2VzTW9kdWxlXCIsIHtcbiAgdmFsdWU6IHRydWVcbn0pO1xuZXhwb3J0cy5UZVggPSB2b2lkIDA7XG52YXIgSW5wdXRKYXhfanNfMSA9IHJlcXVpcmUoXCIuLi9jb3JlL0lucHV0SmF4LmpzXCIpO1xudmFyIE9wdGlvbnNfanNfMSA9IHJlcXVpcmUoXCIuLi91dGlsL09wdGlvbnMuanNcIik7XG52YXIgRmluZFRlWF9qc18xID0gcmVxdWlyZShcIi4vdGV4L0ZpbmRUZVguanNcIik7XG52YXIgRmlsdGVyVXRpbF9qc18xID0gX19pbXBvcnREZWZhdWx0KHJlcXVpcmUoXCIuL3RleC9GaWx0ZXJVdGlsLmpzXCIpKTtcbnZhciBOb2RlVXRpbF9qc18xID0gX19pbXBvcnREZWZhdWx0KHJlcXVpcmUoXCIuL3RleC9Ob2RlVXRpbC5qc1wiKSk7XG52YXIgVGV4UGFyc2VyX2pzXzEgPSBfX2ltcG9ydERlZmF1bHQocmVxdWlyZShcIi4vdGV4L1RleFBhcnNlci5qc1wiKSk7XG52YXIgVGV4RXJyb3JfanNfMSA9IF9faW1wb3J0RGVmYXVsdChyZXF1aXJlKFwiLi90ZXgvVGV4RXJyb3IuanNcIikpO1xudmFyIFBhcnNlT3B0aW9uc19qc18xID0gX19pbXBvcnREZWZhdWx0KHJlcXVpcmUoXCIuL3RleC9QYXJzZU9wdGlvbnMuanNcIikpO1xudmFyIFRhZ3NfanNfMSA9IHJlcXVpcmUoXCIuL3RleC9UYWdzLmpzXCIpO1xudmFyIENvbmZpZ3VyYXRpb25fanNfMSA9IHJlcXVpcmUoXCIuL3RleC9Db25maWd1cmF0aW9uLmpzXCIpO1xucmVxdWlyZShcIi4vdGV4L2Jhc2UvQmFzZUNvbmZpZ3VyYXRpb24uanNcIik7XG52YXIgVGVYID0gZnVuY3Rpb24gKF9zdXBlcikge1xuICBfX2V4dGVuZHMoVGVYLCBfc3VwZXIpO1xuICBmdW5jdGlvbiBUZVgob3B0aW9ucykge1xuICAgIGlmIChvcHRpb25zID09PSB2b2lkIDApIHtcbiAgICAgIG9wdGlvbnMgPSB7fTtcbiAgICB9XG4gICAgdmFyIF90aGlzID0gdGhpcztcbiAgICB2YXIgX2EgPSBfX3JlYWQoKDAsIE9wdGlvbnNfanNfMS5zZXBhcmF0ZU9wdGlvbnMpKG9wdGlvbnMsIFRlWC5PUFRJT05TLCBGaW5kVGVYX2pzXzEuRmluZFRlWC5PUFRJT05TKSwgMyksXG4gICAgICByZXN0ID0gX2FbMF0sXG4gICAgICB0ZXggPSBfYVsxXSxcbiAgICAgIGZpbmQgPSBfYVsyXTtcbiAgICBfdGhpcyA9IF9zdXBlci5jYWxsKHRoaXMsIHRleCkgfHwgdGhpcztcbiAgICBfdGhpcy5maW5kVGVYID0gX3RoaXMub3B0aW9uc1snRmluZFRlWCddIHx8IG5ldyBGaW5kVGVYX2pzXzEuRmluZFRlWChmaW5kKTtcbiAgICB2YXIgcGFja2FnZXMgPSBfdGhpcy5vcHRpb25zLnBhY2thZ2VzO1xuICAgIHZhciBjb25maWd1cmF0aW9uID0gX3RoaXMuY29uZmlndXJhdGlvbiA9IFRlWC5jb25maWd1cmUocGFja2FnZXMpO1xuICAgIHZhciBwYXJzZU9wdGlvbnMgPSBfdGhpcy5fcGFyc2VPcHRpb25zID0gbmV3IFBhcnNlT3B0aW9uc19qc18xLmRlZmF1bHQoY29uZmlndXJhdGlvbiwgW190aGlzLm9wdGlvbnMsIFRhZ3NfanNfMS5UYWdzRmFjdG9yeS5PUFRJT05TXSk7XG4gICAgKDAsIE9wdGlvbnNfanNfMS51c2VyT3B0aW9ucykocGFyc2VPcHRpb25zLm9wdGlvbnMsIHJlc3QpO1xuICAgIGNvbmZpZ3VyYXRpb24uY29uZmlnKF90aGlzKTtcbiAgICBUZVgudGFncyhwYXJzZU9wdGlvbnMsIGNvbmZpZ3VyYXRpb24pO1xuICAgIF90aGlzLnBvc3RGaWx0ZXJzLmFkZChGaWx0ZXJVdGlsX2pzXzEuZGVmYXVsdC5jbGVhblN1YlN1cCwgLTYpO1xuICAgIF90aGlzLnBvc3RGaWx0ZXJzLmFkZChGaWx0ZXJVdGlsX2pzXzEuZGVmYXVsdC5zZXRJbmhlcml0ZWQsIC01KTtcbiAgICBfdGhpcy5wb3N0RmlsdGVycy5hZGQoRmlsdGVyVXRpbF9qc18xLmRlZmF1bHQubW92ZUxpbWl0cywgLTQpO1xuICAgIF90aGlzLnBvc3RGaWx0ZXJzLmFkZChGaWx0ZXJVdGlsX2pzXzEuZGVmYXVsdC5jbGVhblN0cmV0Y2h5LCAtMyk7XG4gICAgX3RoaXMucG9zdEZpbHRlcnMuYWRkKEZpbHRlclV0aWxfanNfMS5kZWZhdWx0LmNsZWFuQXR0cmlidXRlcywgLTIpO1xuICAgIF90aGlzLnBvc3RGaWx0ZXJzLmFkZChGaWx0ZXJVdGlsX2pzXzEuZGVmYXVsdC5jb21iaW5lUmVsYXRpb25zLCAtMSk7XG4gICAgcmV0dXJuIF90aGlzO1xuICB9XG4gIFRlWC5jb25maWd1cmUgPSBmdW5jdGlvbiAocGFja2FnZXMpIHtcbiAgICB2YXIgY29uZmlndXJhdGlvbiA9IG5ldyBDb25maWd1cmF0aW9uX2pzXzEuUGFyc2VyQ29uZmlndXJhdGlvbihwYWNrYWdlcywgWyd0ZXgnXSk7XG4gICAgY29uZmlndXJhdGlvbi5pbml0KCk7XG4gICAgcmV0dXJuIGNvbmZpZ3VyYXRpb247XG4gIH07XG4gIFRlWC50YWdzID0gZnVuY3Rpb24gKG9wdGlvbnMsIGNvbmZpZ3VyYXRpb24pIHtcbiAgICBUYWdzX2pzXzEuVGFnc0ZhY3RvcnkuYWRkVGFncyhjb25maWd1cmF0aW9uLnRhZ3MpO1xuICAgIFRhZ3NfanNfMS5UYWdzRmFjdG9yeS5zZXREZWZhdWx0KG9wdGlvbnMub3B0aW9ucy50YWdzKTtcbiAgICBvcHRpb25zLnRhZ3MgPSBUYWdzX2pzXzEuVGFnc0ZhY3RvcnkuZ2V0RGVmYXVsdCgpO1xuICAgIG9wdGlvbnMudGFncy5jb25maWd1cmF0aW9uID0gb3B0aW9ucztcbiAgfTtcbiAgVGVYLnByb3RvdHlwZS5zZXRNbWxGYWN0b3J5ID0gZnVuY3Rpb24gKG1tbEZhY3RvcnkpIHtcbiAgICBfc3VwZXIucHJvdG90eXBlLnNldE1tbEZhY3RvcnkuY2FsbCh0aGlzLCBtbWxGYWN0b3J5KTtcbiAgICB0aGlzLl9wYXJzZU9wdGlvbnMubm9kZUZhY3Rvcnkuc2V0TW1sRmFjdG9yeShtbWxGYWN0b3J5KTtcbiAgfTtcbiAgT2JqZWN0LmRlZmluZVByb3BlcnR5KFRlWC5wcm90b3R5cGUsIFwicGFyc2VPcHRpb25zXCIsIHtcbiAgICBnZXQ6IGZ1bmN0aW9uICgpIHtcbiAgICAgIHJldHVybiB0aGlzLl9wYXJzZU9wdGlvbnM7XG4gICAgfSxcbiAgICBlbnVtZXJhYmxlOiBmYWxzZSxcbiAgICBjb25maWd1cmFibGU6IHRydWVcbiAgfSk7XG4gIFRlWC5wcm90b3R5cGUucmVzZXQgPSBmdW5jdGlvbiAodGFnKSB7XG4gICAgaWYgKHRhZyA9PT0gdm9pZCAwKSB7XG4gICAgICB0YWcgPSAwO1xuICAgIH1cbiAgICB0aGlzLnBhcnNlT3B0aW9ucy50YWdzLnJlc2V0KHRhZyk7XG4gIH07XG4gIFRlWC5wcm90b3R5cGUuY29tcGlsZSA9IGZ1bmN0aW9uIChtYXRoLCBkb2N1bWVudCkge1xuICAgIHRoaXMucGFyc2VPcHRpb25zLmNsZWFyKCk7XG4gICAgdGhpcy5leGVjdXRlRmlsdGVycyh0aGlzLnByZUZpbHRlcnMsIG1hdGgsIGRvY3VtZW50LCB0aGlzLnBhcnNlT3B0aW9ucyk7XG4gICAgdmFyIGRpc3BsYXkgPSBtYXRoLmRpc3BsYXk7XG4gICAgdGhpcy5sYXRleCA9IG1hdGgubWF0aDtcbiAgICB2YXIgbm9kZTtcbiAgICB0aGlzLnBhcnNlT3B0aW9ucy50YWdzLnN0YXJ0RXF1YXRpb24obWF0aCk7XG4gICAgdmFyIGdsb2JhbEVudjtcbiAgICB0cnkge1xuICAgICAgdmFyIHBhcnNlciA9IG5ldyBUZXhQYXJzZXJfanNfMS5kZWZhdWx0KHRoaXMubGF0ZXgsIHtcbiAgICAgICAgZGlzcGxheTogZGlzcGxheSxcbiAgICAgICAgaXNJbm5lcjogZmFsc2VcbiAgICAgIH0sIHRoaXMucGFyc2VPcHRpb25zKTtcbiAgICAgIG5vZGUgPSBwYXJzZXIubW1sKCk7XG4gICAgICBnbG9iYWxFbnYgPSBwYXJzZXIuc3RhY2suZ2xvYmFsO1xuICAgIH0gY2F0Y2ggKGVycikge1xuICAgICAgaWYgKCEoZXJyIGluc3RhbmNlb2YgVGV4RXJyb3JfanNfMS5kZWZhdWx0KSkge1xuICAgICAgICB0aHJvdyBlcnI7XG4gICAgICB9XG4gICAgICB0aGlzLnBhcnNlT3B0aW9ucy5lcnJvciA9IHRydWU7XG4gICAgICBub2RlID0gdGhpcy5vcHRpb25zLmZvcm1hdEVycm9yKHRoaXMsIGVycik7XG4gICAgfVxuICAgIG5vZGUgPSB0aGlzLnBhcnNlT3B0aW9ucy5ub2RlRmFjdG9yeS5jcmVhdGUoJ25vZGUnLCAnbWF0aCcsIFtub2RlXSk7XG4gICAgaWYgKGdsb2JhbEVudiA9PT0gbnVsbCB8fCBnbG9iYWxFbnYgPT09IHZvaWQgMCA/IHZvaWQgMCA6IGdsb2JhbEVudi5pbmRlbnRhbGlnbikge1xuICAgICAgTm9kZVV0aWxfanNfMS5kZWZhdWx0LnNldEF0dHJpYnV0ZShub2RlLCAnaW5kZW50YWxpZ24nLCBnbG9iYWxFbnYuaW5kZW50YWxpZ24pO1xuICAgIH1cbiAgICBpZiAoZGlzcGxheSkge1xuICAgICAgTm9kZVV0aWxfanNfMS5kZWZhdWx0LnNldEF0dHJpYnV0ZShub2RlLCAnZGlzcGxheScsICdibG9jaycpO1xuICAgIH1cbiAgICB0aGlzLnBhcnNlT3B0aW9ucy50YWdzLmZpbmlzaEVxdWF0aW9uKG1hdGgpO1xuICAgIHRoaXMucGFyc2VPcHRpb25zLnJvb3QgPSBub2RlO1xuICAgIHRoaXMuZXhlY3V0ZUZpbHRlcnModGhpcy5wb3N0RmlsdGVycywgbWF0aCwgZG9jdW1lbnQsIHRoaXMucGFyc2VPcHRpb25zKTtcbiAgICB0aGlzLm1hdGhOb2RlID0gdGhpcy5wYXJzZU9wdGlvbnMucm9vdDtcbiAgICByZXR1cm4gdGhpcy5tYXRoTm9kZTtcbiAgfTtcbiAgVGVYLnByb3RvdHlwZS5maW5kTWF0aCA9IGZ1bmN0aW9uIChzdHJpbmdzKSB7XG4gICAgcmV0dXJuIHRoaXMuZmluZFRlWC5maW5kTWF0aChzdHJpbmdzKTtcbiAgfTtcbiAgVGVYLnByb3RvdHlwZS5mb3JtYXRFcnJvciA9IGZ1bmN0aW9uIChlcnIpIHtcbiAgICB2YXIgbWVzc2FnZSA9IGVyci5tZXNzYWdlLnJlcGxhY2UoL1xcbi4qLywgJycpO1xuICAgIHJldHVybiB0aGlzLnBhcnNlT3B0aW9ucy5ub2RlRmFjdG9yeS5jcmVhdGUoJ2Vycm9yJywgbWVzc2FnZSwgZXJyLmlkLCB0aGlzLmxhdGV4KTtcbiAgfTtcbiAgVGVYLk5BTUUgPSAnVGVYJztcbiAgVGVYLk9QVElPTlMgPSBfX2Fzc2lnbihfX2Fzc2lnbih7fSwgSW5wdXRKYXhfanNfMS5BYnN0cmFjdElucHV0SmF4Lk9QVElPTlMpLCB7XG4gICAgRmluZFRlWDogbnVsbCxcbiAgICBwYWNrYWdlczogWydiYXNlJ10sXG4gICAgZGlnaXRzOiAvXig/OlswLTldKyg/OlxceyxcXH1bMC05XXszfSkqKD86XFwuWzAtOV0qKT98XFwuWzAtOV0rKS8sXG4gICAgbWF4QnVmZmVyOiA1ICogMTAyNCxcbiAgICBmb3JtYXRFcnJvcjogZnVuY3Rpb24gKGpheCwgZXJyKSB7XG4gICAgICByZXR1cm4gamF4LmZvcm1hdEVycm9yKGVycik7XG4gICAgfVxuICB9KTtcbiAgcmV0dXJuIFRlWDtcbn0oSW5wdXRKYXhfanNfMS5BYnN0cmFjdElucHV0SmF4KTtcbmV4cG9ydHMuVGVYID0gVGVYOyIsIlwidXNlIHN0cmljdFwiO1xuXG52YXIgX192YWx1ZXMgPSB0aGlzICYmIHRoaXMuX192YWx1ZXMgfHwgZnVuY3Rpb24gKG8pIHtcbiAgdmFyIHMgPSB0eXBlb2YgU3ltYm9sID09PSBcImZ1bmN0aW9uXCIgJiYgU3ltYm9sLml0ZXJhdG9yLFxuICAgIG0gPSBzICYmIG9bc10sXG4gICAgaSA9IDA7XG4gIGlmIChtKSByZXR1cm4gbS5jYWxsKG8pO1xuICBpZiAobyAmJiB0eXBlb2Ygby5sZW5ndGggPT09IFwibnVtYmVyXCIpIHJldHVybiB7XG4gICAgbmV4dDogZnVuY3Rpb24gKCkge1xuICAgICAgaWYgKG8gJiYgaSA+PSBvLmxlbmd0aCkgbyA9IHZvaWQgMDtcbiAgICAgIHJldHVybiB7XG4gICAgICAgIHZhbHVlOiBvICYmIG9baSsrXSxcbiAgICAgICAgZG9uZTogIW9cbiAgICAgIH07XG4gICAgfVxuICB9O1xuICB0aHJvdyBuZXcgVHlwZUVycm9yKHMgPyBcIk9iamVjdCBpcyBub3QgaXRlcmFibGUuXCIgOiBcIlN5bWJvbC5pdGVyYXRvciBpcyBub3QgZGVmaW5lZC5cIik7XG59O1xudmFyIF9faW1wb3J0RGVmYXVsdCA9IHRoaXMgJiYgdGhpcy5fX2ltcG9ydERlZmF1bHQgfHwgZnVuY3Rpb24gKG1vZCkge1xuICByZXR1cm4gbW9kICYmIG1vZC5fX2VzTW9kdWxlID8gbW9kIDoge1xuICAgIFwiZGVmYXVsdFwiOiBtb2RcbiAgfTtcbn07XG5PYmplY3QuZGVmaW5lUHJvcGVydHkoZXhwb3J0cywgXCJfX2VzTW9kdWxlXCIsIHtcbiAgdmFsdWU6IHRydWVcbn0pO1xudmFyIE1tbE5vZGVfanNfMSA9IHJlcXVpcmUoXCIuLi8uLi9jb3JlL01tbFRyZWUvTW1sTm9kZS5qc1wiKTtcbnZhciBOb2RlVXRpbF9qc18xID0gX19pbXBvcnREZWZhdWx0KHJlcXVpcmUoXCIuL05vZGVVdGlsLmpzXCIpKTtcbnZhciBGaWx0ZXJVdGlsO1xuKGZ1bmN0aW9uIChGaWx0ZXJVdGlsKSB7XG4gIEZpbHRlclV0aWwuY2xlYW5TdHJldGNoeSA9IGZ1bmN0aW9uIChhcmcpIHtcbiAgICB2YXIgZV8xLCBfYTtcbiAgICB2YXIgb3B0aW9ucyA9IGFyZy5kYXRhO1xuICAgIHRyeSB7XG4gICAgICBmb3IgKHZhciBfYiA9IF9fdmFsdWVzKG9wdGlvbnMuZ2V0TGlzdCgnZml4U3RyZXRjaHknKSksIF9jID0gX2IubmV4dCgpOyAhX2MuZG9uZTsgX2MgPSBfYi5uZXh0KCkpIHtcbiAgICAgICAgdmFyIG1vID0gX2MudmFsdWU7XG4gICAgICAgIGlmIChOb2RlVXRpbF9qc18xLmRlZmF1bHQuZ2V0UHJvcGVydHkobW8sICdmaXhTdHJldGNoeScpKSB7XG4gICAgICAgICAgdmFyIHN5bWJvbCA9IE5vZGVVdGlsX2pzXzEuZGVmYXVsdC5nZXRGb3JtKG1vKTtcbiAgICAgICAgICBpZiAoc3ltYm9sICYmIHN5bWJvbFszXSAmJiBzeW1ib2xbM11bJ3N0cmV0Y2h5J10pIHtcbiAgICAgICAgICAgIE5vZGVVdGlsX2pzXzEuZGVmYXVsdC5zZXRBdHRyaWJ1dGUobW8sICdzdHJldGNoeScsIGZhbHNlKTtcbiAgICAgICAgICB9XG4gICAgICAgICAgdmFyIHBhcmVudF8xID0gbW8ucGFyZW50O1xuICAgICAgICAgIGlmICghTm9kZVV0aWxfanNfMS5kZWZhdWx0LmdldFRleENsYXNzKG1vKSAmJiAoIXN5bWJvbCB8fCAhc3ltYm9sWzJdKSkge1xuICAgICAgICAgICAgdmFyIHRleEF0b20gPSBvcHRpb25zLm5vZGVGYWN0b3J5LmNyZWF0ZSgnbm9kZScsICdUZVhBdG9tJywgW21vXSk7XG4gICAgICAgICAgICBwYXJlbnRfMS5yZXBsYWNlQ2hpbGQodGV4QXRvbSwgbW8pO1xuICAgICAgICAgICAgdGV4QXRvbS5pbmhlcml0QXR0cmlidXRlc0Zyb20obW8pO1xuICAgICAgICAgIH1cbiAgICAgICAgICBOb2RlVXRpbF9qc18xLmRlZmF1bHQucmVtb3ZlUHJvcGVydGllcyhtbywgJ2ZpeFN0cmV0Y2h5Jyk7XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9IGNhdGNoIChlXzFfMSkge1xuICAgICAgZV8xID0ge1xuICAgICAgICBlcnJvcjogZV8xXzFcbiAgICAgIH07XG4gICAgfSBmaW5hbGx5IHtcbiAgICAgIHRyeSB7XG4gICAgICAgIGlmIChfYyAmJiAhX2MuZG9uZSAmJiAoX2EgPSBfYi5yZXR1cm4pKSBfYS5jYWxsKF9iKTtcbiAgICAgIH0gZmluYWxseSB7XG4gICAgICAgIGlmIChlXzEpIHRocm93IGVfMS5lcnJvcjtcbiAgICAgIH1cbiAgICB9XG4gIH07XG4gIEZpbHRlclV0aWwuY2xlYW5BdHRyaWJ1dGVzID0gZnVuY3Rpb24gKGFyZykge1xuICAgIHZhciBub2RlID0gYXJnLmRhdGEucm9vdDtcbiAgICBub2RlLndhbGtUcmVlKGZ1bmN0aW9uIChtbWwsIF9kKSB7XG4gICAgICB2YXIgZV8yLCBfYTtcbiAgICAgIHZhciBhdHRyaWJzID0gbW1sLmF0dHJpYnV0ZXM7XG4gICAgICBpZiAoIWF0dHJpYnMpIHtcbiAgICAgICAgcmV0dXJuO1xuICAgICAgfVxuICAgICAgdmFyIGtlZXAgPSBuZXcgU2V0KChhdHRyaWJzLmdldCgnbWp4LWtlZXAtYXR0cnMnKSB8fCAnJykuc3BsaXQoLyAvKSk7XG4gICAgICBkZWxldGUgYXR0cmlicy5nZXRBbGxBdHRyaWJ1dGVzKClbJ21qeC1rZWVwLWF0dHJzJ107XG4gICAgICB0cnkge1xuICAgICAgICBmb3IgKHZhciBfYiA9IF9fdmFsdWVzKGF0dHJpYnMuZ2V0RXhwbGljaXROYW1lcygpKSwgX2MgPSBfYi5uZXh0KCk7ICFfYy5kb25lOyBfYyA9IF9iLm5leHQoKSkge1xuICAgICAgICAgIHZhciBrZXkgPSBfYy52YWx1ZTtcbiAgICAgICAgICBpZiAoIWtlZXAuaGFzKGtleSkgJiYgYXR0cmlicy5hdHRyaWJ1dGVzW2tleV0gPT09IG1tbC5hdHRyaWJ1dGVzLmdldEluaGVyaXRlZChrZXkpKSB7XG4gICAgICAgICAgICBkZWxldGUgYXR0cmlicy5hdHRyaWJ1dGVzW2tleV07XG4gICAgICAgICAgfVxuICAgICAgICB9XG4gICAgICB9IGNhdGNoIChlXzJfMSkge1xuICAgICAgICBlXzIgPSB7XG4gICAgICAgICAgZXJyb3I6IGVfMl8xXG4gICAgICAgIH07XG4gICAgICB9IGZpbmFsbHkge1xuICAgICAgICB0cnkge1xuICAgICAgICAgIGlmIChfYyAmJiAhX2MuZG9uZSAmJiAoX2EgPSBfYi5yZXR1cm4pKSBfYS5jYWxsKF9iKTtcbiAgICAgICAgfSBmaW5hbGx5IHtcbiAgICAgICAgICBpZiAoZV8yKSB0aHJvdyBlXzIuZXJyb3I7XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9LCB7fSk7XG4gIH07XG4gIEZpbHRlclV0aWwuY29tYmluZVJlbGF0aW9ucyA9IGZ1bmN0aW9uIChhcmcpIHtcbiAgICB2YXIgZV8zLCBfYSwgZV80LCBfYjtcbiAgICB2YXIgcmVtb3ZlID0gW107XG4gICAgdHJ5IHtcbiAgICAgIGZvciAodmFyIF9jID0gX192YWx1ZXMoYXJnLmRhdGEuZ2V0TGlzdCgnbW8nKSksIF9lID0gX2MubmV4dCgpOyAhX2UuZG9uZTsgX2UgPSBfYy5uZXh0KCkpIHtcbiAgICAgICAgdmFyIG1vID0gX2UudmFsdWU7XG4gICAgICAgIGlmIChtby5nZXRQcm9wZXJ0eSgncmVsYXRpb25zQ29tYmluZWQnKSB8fCAhbW8ucGFyZW50IHx8IG1vLnBhcmVudCAmJiAhTm9kZVV0aWxfanNfMS5kZWZhdWx0LmlzVHlwZShtby5wYXJlbnQsICdtcm93JykgfHwgTm9kZVV0aWxfanNfMS5kZWZhdWx0LmdldFRleENsYXNzKG1vKSAhPT0gTW1sTm9kZV9qc18xLlRFWENMQVNTLlJFTCkge1xuICAgICAgICAgIGNvbnRpbnVlO1xuICAgICAgICB9XG4gICAgICAgIHZhciBtbWwgPSBtby5wYXJlbnQ7XG4gICAgICAgIHZhciBtMiA9IHZvaWQgMDtcbiAgICAgICAgdmFyIGNoaWxkcmVuID0gbW1sLmNoaWxkTm9kZXM7XG4gICAgICAgIHZhciBuZXh0ID0gY2hpbGRyZW4uaW5kZXhPZihtbykgKyAxO1xuICAgICAgICB2YXIgdmFyaWFudEZvcm0gPSBOb2RlVXRpbF9qc18xLmRlZmF1bHQuZ2V0UHJvcGVydHkobW8sICd2YXJpYW50Rm9ybScpO1xuICAgICAgICB3aGlsZSAobmV4dCA8IGNoaWxkcmVuLmxlbmd0aCAmJiAobTIgPSBjaGlsZHJlbltuZXh0XSkgJiYgTm9kZVV0aWxfanNfMS5kZWZhdWx0LmlzVHlwZShtMiwgJ21vJykgJiYgTm9kZVV0aWxfanNfMS5kZWZhdWx0LmdldFRleENsYXNzKG0yKSA9PT0gTW1sTm9kZV9qc18xLlRFWENMQVNTLlJFTCkge1xuICAgICAgICAgIGlmICh2YXJpYW50Rm9ybSA9PT0gTm9kZVV0aWxfanNfMS5kZWZhdWx0LmdldFByb3BlcnR5KG0yLCAndmFyaWFudEZvcm0nKSAmJiBfY29tcGFyZUV4cGxpY2l0KG1vLCBtMikpIHtcbiAgICAgICAgICAgIE5vZGVVdGlsX2pzXzEuZGVmYXVsdC5hcHBlbmRDaGlsZHJlbihtbywgTm9kZVV0aWxfanNfMS5kZWZhdWx0LmdldENoaWxkcmVuKG0yKSk7XG4gICAgICAgICAgICBfY29weUV4cGxpY2l0KFsnc3RyZXRjaHknLCAncnNwYWNlJ10sIG1vLCBtMik7XG4gICAgICAgICAgICB0cnkge1xuICAgICAgICAgICAgICBmb3IgKHZhciBfZiA9IChlXzQgPSB2b2lkIDAsIF9fdmFsdWVzKG0yLmdldFByb3BlcnR5TmFtZXMoKSkpLCBfZyA9IF9mLm5leHQoKTsgIV9nLmRvbmU7IF9nID0gX2YubmV4dCgpKSB7XG4gICAgICAgICAgICAgICAgdmFyIG5hbWVfMSA9IF9nLnZhbHVlO1xuICAgICAgICAgICAgICAgIG1vLnNldFByb3BlcnR5KG5hbWVfMSwgbTIuZ2V0UHJvcGVydHkobmFtZV8xKSk7XG4gICAgICAgICAgICAgIH1cbiAgICAgICAgICAgIH0gY2F0Y2ggKGVfNF8xKSB7XG4gICAgICAgICAgICAgIGVfNCA9IHtcbiAgICAgICAgICAgICAgICBlcnJvcjogZV80XzFcbiAgICAgICAgICAgICAgfTtcbiAgICAgICAgICAgIH0gZmluYWxseSB7XG4gICAgICAgICAgICAgIHRyeSB7XG4gICAgICAgICAgICAgICAgaWYgKF9nICYmICFfZy5kb25lICYmIChfYiA9IF9mLnJldHVybikpIF9iLmNhbGwoX2YpO1xuICAgICAgICAgICAgICB9IGZpbmFsbHkge1xuICAgICAgICAgICAgICAgIGlmIChlXzQpIHRocm93IGVfNC5lcnJvcjtcbiAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgfVxuICAgICAgICAgICAgY2hpbGRyZW4uc3BsaWNlKG5leHQsIDEpO1xuICAgICAgICAgICAgcmVtb3ZlLnB1c2gobTIpO1xuICAgICAgICAgICAgbTIucGFyZW50ID0gbnVsbDtcbiAgICAgICAgICAgIG0yLnNldFByb3BlcnR5KCdyZWxhdGlvbnNDb21iaW5lZCcsIHRydWUpO1xuICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICBpZiAobW8uYXR0cmlidXRlcy5nZXRFeHBsaWNpdCgncnNwYWNlJykgPT0gbnVsbCkge1xuICAgICAgICAgICAgICBOb2RlVXRpbF9qc18xLmRlZmF1bHQuc2V0QXR0cmlidXRlKG1vLCAncnNwYWNlJywgJzBwdCcpO1xuICAgICAgICAgICAgfVxuICAgICAgICAgICAgaWYgKG0yLmF0dHJpYnV0ZXMuZ2V0RXhwbGljaXQoJ2xzcGFjZScpID09IG51bGwpIHtcbiAgICAgICAgICAgICAgTm9kZVV0aWxfanNfMS5kZWZhdWx0LnNldEF0dHJpYnV0ZShtMiwgJ2xzcGFjZScsICcwcHQnKTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgICAgIGJyZWFrO1xuICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgICAgICBtby5hdHRyaWJ1dGVzLnNldEluaGVyaXRlZCgnZm9ybScsIG1vLmdldEZvcm1zKClbMF0pO1xuICAgICAgfVxuICAgIH0gY2F0Y2ggKGVfM18xKSB7XG4gICAgICBlXzMgPSB7XG4gICAgICAgIGVycm9yOiBlXzNfMVxuICAgICAgfTtcbiAgICB9IGZpbmFsbHkge1xuICAgICAgdHJ5IHtcbiAgICAgICAgaWYgKF9lICYmICFfZS5kb25lICYmIChfYSA9IF9jLnJldHVybikpIF9hLmNhbGwoX2MpO1xuICAgICAgfSBmaW5hbGx5IHtcbiAgICAgICAgaWYgKGVfMykgdGhyb3cgZV8zLmVycm9yO1xuICAgICAgfVxuICAgIH1cbiAgICBhcmcuZGF0YS5yZW1vdmVGcm9tTGlzdCgnbW8nLCByZW1vdmUpO1xuICB9O1xuICB2YXIgX2NvcHlFeHBsaWNpdCA9IGZ1bmN0aW9uIChhdHRycywgbm9kZTEsIG5vZGUyKSB7XG4gICAgdmFyIGF0dHIxID0gbm9kZTEuYXR0cmlidXRlcztcbiAgICB2YXIgYXR0cjIgPSBub2RlMi5hdHRyaWJ1dGVzO1xuICAgIGF0dHJzLmZvckVhY2goZnVuY3Rpb24gKHgpIHtcbiAgICAgIHZhciBhdHRyID0gYXR0cjIuZ2V0RXhwbGljaXQoeCk7XG4gICAgICBpZiAoYXR0ciAhPSBudWxsKSB7XG4gICAgICAgIGF0dHIxLnNldCh4LCBhdHRyKTtcbiAgICAgIH1cbiAgICB9KTtcbiAgfTtcbiAgdmFyIF9jb21wYXJlRXhwbGljaXQgPSBmdW5jdGlvbiAobm9kZTEsIG5vZGUyKSB7XG4gICAgdmFyIGVfNSwgX2E7XG4gICAgdmFyIGZpbHRlciA9IGZ1bmN0aW9uIChhdHRyLCBzcGFjZSkge1xuICAgICAgdmFyIGV4cCA9IGF0dHIuZ2V0RXhwbGljaXROYW1lcygpO1xuICAgICAgcmV0dXJuIGV4cC5maWx0ZXIoZnVuY3Rpb24gKHgpIHtcbiAgICAgICAgcmV0dXJuIHggIT09IHNwYWNlICYmICh4ICE9PSAnc3RyZXRjaHknIHx8IGF0dHIuZ2V0RXhwbGljaXQoJ3N0cmV0Y2h5JykpO1xuICAgICAgfSk7XG4gICAgfTtcbiAgICB2YXIgYXR0cjEgPSBub2RlMS5hdHRyaWJ1dGVzO1xuICAgIHZhciBhdHRyMiA9IG5vZGUyLmF0dHJpYnV0ZXM7XG4gICAgdmFyIGV4cDEgPSBmaWx0ZXIoYXR0cjEsICdsc3BhY2UnKTtcbiAgICB2YXIgZXhwMiA9IGZpbHRlcihhdHRyMiwgJ3JzcGFjZScpO1xuICAgIGlmIChleHAxLmxlbmd0aCAhPT0gZXhwMi5sZW5ndGgpIHtcbiAgICAgIHJldHVybiBmYWxzZTtcbiAgICB9XG4gICAgdHJ5IHtcbiAgICAgIGZvciAodmFyIGV4cDFfMSA9IF9fdmFsdWVzKGV4cDEpLCBleHAxXzFfMSA9IGV4cDFfMS5uZXh0KCk7ICFleHAxXzFfMS5kb25lOyBleHAxXzFfMSA9IGV4cDFfMS5uZXh0KCkpIHtcbiAgICAgICAgdmFyIG5hbWVfMiA9IGV4cDFfMV8xLnZhbHVlO1xuICAgICAgICBpZiAoYXR0cjEuZ2V0RXhwbGljaXQobmFtZV8yKSAhPT0gYXR0cjIuZ2V0RXhwbGljaXQobmFtZV8yKSkge1xuICAgICAgICAgIHJldHVybiBmYWxzZTtcbiAgICAgICAgfVxuICAgICAgfVxuICAgIH0gY2F0Y2ggKGVfNV8xKSB7XG4gICAgICBlXzUgPSB7XG4gICAgICAgIGVycm9yOiBlXzVfMVxuICAgICAgfTtcbiAgICB9IGZpbmFsbHkge1xuICAgICAgdHJ5IHtcbiAgICAgICAgaWYgKGV4cDFfMV8xICYmICFleHAxXzFfMS5kb25lICYmIChfYSA9IGV4cDFfMS5yZXR1cm4pKSBfYS5jYWxsKGV4cDFfMSk7XG4gICAgICB9IGZpbmFsbHkge1xuICAgICAgICBpZiAoZV81KSB0aHJvdyBlXzUuZXJyb3I7XG4gICAgICB9XG4gICAgfVxuICAgIHJldHVybiB0cnVlO1xuICB9O1xuICB2YXIgX2NsZWFuU3ViU3VwID0gZnVuY3Rpb24gKG9wdGlvbnMsIGxvdywgdXApIHtcbiAgICB2YXIgZV82LCBfYTtcbiAgICB2YXIgcmVtb3ZlID0gW107XG4gICAgdHJ5IHtcbiAgICAgIGZvciAodmFyIF9iID0gX192YWx1ZXMob3B0aW9ucy5nZXRMaXN0KCdtJyArIGxvdyArIHVwKSksIF9jID0gX2IubmV4dCgpOyAhX2MuZG9uZTsgX2MgPSBfYi5uZXh0KCkpIHtcbiAgICAgICAgdmFyIG1tbCA9IF9jLnZhbHVlO1xuICAgICAgICB2YXIgY2hpbGRyZW4gPSBtbWwuY2hpbGROb2RlcztcbiAgICAgICAgaWYgKGNoaWxkcmVuW21tbFtsb3ddXSAmJiBjaGlsZHJlblttbWxbdXBdXSkge1xuICAgICAgICAgIGNvbnRpbnVlO1xuICAgICAgICB9XG4gICAgICAgIHZhciBwYXJlbnRfMiA9IG1tbC5wYXJlbnQ7XG4gICAgICAgIHZhciBuZXdOb2RlID0gY2hpbGRyZW5bbW1sW2xvd11dID8gb3B0aW9ucy5ub2RlRmFjdG9yeS5jcmVhdGUoJ25vZGUnLCAnbScgKyBsb3csIFtjaGlsZHJlblttbWwuYmFzZV0sIGNoaWxkcmVuW21tbFtsb3ddXV0pIDogb3B0aW9ucy5ub2RlRmFjdG9yeS5jcmVhdGUoJ25vZGUnLCAnbScgKyB1cCwgW2NoaWxkcmVuW21tbC5iYXNlXSwgY2hpbGRyZW5bbW1sW3VwXV1dKTtcbiAgICAgICAgTm9kZVV0aWxfanNfMS5kZWZhdWx0LmNvcHlBdHRyaWJ1dGVzKG1tbCwgbmV3Tm9kZSk7XG4gICAgICAgIGlmIChwYXJlbnRfMikge1xuICAgICAgICAgIHBhcmVudF8yLnJlcGxhY2VDaGlsZChuZXdOb2RlLCBtbWwpO1xuICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgIG9wdGlvbnMucm9vdCA9IG5ld05vZGU7XG4gICAgICAgIH1cbiAgICAgICAgcmVtb3ZlLnB1c2gobW1sKTtcbiAgICAgIH1cbiAgICB9IGNhdGNoIChlXzZfMSkge1xuICAgICAgZV82ID0ge1xuICAgICAgICBlcnJvcjogZV82XzFcbiAgICAgIH07XG4gICAgfSBmaW5hbGx5IHtcbiAgICAgIHRyeSB7XG4gICAgICAgIGlmIChfYyAmJiAhX2MuZG9uZSAmJiAoX2EgPSBfYi5yZXR1cm4pKSBfYS5jYWxsKF9iKTtcbiAgICAgIH0gZmluYWxseSB7XG4gICAgICAgIGlmIChlXzYpIHRocm93IGVfNi5lcnJvcjtcbiAgICAgIH1cbiAgICB9XG4gICAgb3B0aW9ucy5yZW1vdmVGcm9tTGlzdCgnbScgKyBsb3cgKyB1cCwgcmVtb3ZlKTtcbiAgfTtcbiAgRmlsdGVyVXRpbC5jbGVhblN1YlN1cCA9IGZ1bmN0aW9uIChhcmcpIHtcbiAgICB2YXIgb3B0aW9ucyA9IGFyZy5kYXRhO1xuICAgIGlmIChvcHRpb25zLmVycm9yKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIF9jbGVhblN1YlN1cChvcHRpb25zLCAnc3ViJywgJ3N1cCcpO1xuICAgIF9jbGVhblN1YlN1cChvcHRpb25zLCAndW5kZXInLCAnb3ZlcicpO1xuICB9O1xuICB2YXIgX21vdmVMaW1pdHMgPSBmdW5jdGlvbiAob3B0aW9ucywgdW5kZXJvdmVyLCBzdWJzdXApIHtcbiAgICB2YXIgZV83LCBfYTtcbiAgICB2YXIgcmVtb3ZlID0gW107XG4gICAgdHJ5IHtcbiAgICAgIGZvciAodmFyIF9iID0gX192YWx1ZXMob3B0aW9ucy5nZXRMaXN0KHVuZGVyb3ZlcikpLCBfYyA9IF9iLm5leHQoKTsgIV9jLmRvbmU7IF9jID0gX2IubmV4dCgpKSB7XG4gICAgICAgIHZhciBtbWwgPSBfYy52YWx1ZTtcbiAgICAgICAgaWYgKG1tbC5hdHRyaWJ1dGVzLmdldCgnZGlzcGxheXN0eWxlJykpIHtcbiAgICAgICAgICBjb250aW51ZTtcbiAgICAgICAgfVxuICAgICAgICB2YXIgYmFzZSA9IG1tbC5jaGlsZE5vZGVzW21tbC5iYXNlXTtcbiAgICAgICAgdmFyIG1vID0gYmFzZS5jb3JlTU8oKTtcbiAgICAgICAgaWYgKGJhc2UuZ2V0UHJvcGVydHkoJ21vdmFibGVsaW1pdHMnKSAmJiAhbW8uYXR0cmlidXRlcy5nZXRFeHBsaWNpdCgnbW92YWJsZWxpbWl0cycpKSB7XG4gICAgICAgICAgdmFyIG5vZGUgPSBvcHRpb25zLm5vZGVGYWN0b3J5LmNyZWF0ZSgnbm9kZScsIHN1YnN1cCwgbW1sLmNoaWxkTm9kZXMpO1xuICAgICAgICAgIE5vZGVVdGlsX2pzXzEuZGVmYXVsdC5jb3B5QXR0cmlidXRlcyhtbWwsIG5vZGUpO1xuICAgICAgICAgIGlmIChtbWwucGFyZW50KSB7XG4gICAgICAgICAgICBtbWwucGFyZW50LnJlcGxhY2VDaGlsZChub2RlLCBtbWwpO1xuICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICBvcHRpb25zLnJvb3QgPSBub2RlO1xuICAgICAgICAgIH1cbiAgICAgICAgICByZW1vdmUucHVzaChtbWwpO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgfSBjYXRjaCAoZV83XzEpIHtcbiAgICAgIGVfNyA9IHtcbiAgICAgICAgZXJyb3I6IGVfN18xXG4gICAgICB9O1xuICAgIH0gZmluYWxseSB7XG4gICAgICB0cnkge1xuICAgICAgICBpZiAoX2MgJiYgIV9jLmRvbmUgJiYgKF9hID0gX2IucmV0dXJuKSkgX2EuY2FsbChfYik7XG4gICAgICB9IGZpbmFsbHkge1xuICAgICAgICBpZiAoZV83KSB0aHJvdyBlXzcuZXJyb3I7XG4gICAgICB9XG4gICAgfVxuICAgIG9wdGlvbnMucmVtb3ZlRnJvbUxpc3QodW5kZXJvdmVyLCByZW1vdmUpO1xuICB9O1xuICBGaWx0ZXJVdGlsLm1vdmVMaW1pdHMgPSBmdW5jdGlvbiAoYXJnKSB7XG4gICAgdmFyIG9wdGlvbnMgPSBhcmcuZGF0YTtcbiAgICBfbW92ZUxpbWl0cyhvcHRpb25zLCAnbXVuZGVyb3ZlcicsICdtc3Vic3VwJyk7XG4gICAgX21vdmVMaW1pdHMob3B0aW9ucywgJ211bmRlcicsICdtc3ViJyk7XG4gICAgX21vdmVMaW1pdHMob3B0aW9ucywgJ21vdmVyJywgJ21zdXAnKTtcbiAgfTtcbiAgRmlsdGVyVXRpbC5zZXRJbmhlcml0ZWQgPSBmdW5jdGlvbiAoYXJnKSB7XG4gICAgYXJnLmRhdGEucm9vdC5zZXRJbmhlcml0ZWRBdHRyaWJ1dGVzKHt9LCBhcmcubWF0aFsnZGlzcGxheSddLCAwLCBmYWxzZSk7XG4gIH07XG59KShGaWx0ZXJVdGlsIHx8IChGaWx0ZXJVdGlsID0ge30pKTtcbmV4cG9ydHMuZGVmYXVsdCA9IEZpbHRlclV0aWw7IiwiXCJ1c2Ugc3RyaWN0XCI7XG5cbnZhciBfX2V4dGVuZHMgPSB0aGlzICYmIHRoaXMuX19leHRlbmRzIHx8IGZ1bmN0aW9uICgpIHtcbiAgdmFyIGV4dGVuZFN0YXRpY3MgPSBmdW5jdGlvbiAoZCwgYikge1xuICAgIGV4dGVuZFN0YXRpY3MgPSBPYmplY3Quc2V0UHJvdG90eXBlT2YgfHwge1xuICAgICAgX19wcm90b19fOiBbXVxuICAgIH0gaW5zdGFuY2VvZiBBcnJheSAmJiBmdW5jdGlvbiAoZCwgYikge1xuICAgICAgZC5fX3Byb3RvX18gPSBiO1xuICAgIH0gfHwgZnVuY3Rpb24gKGQsIGIpIHtcbiAgICAgIGZvciAodmFyIHAgaW4gYikgaWYgKE9iamVjdC5wcm90b3R5cGUuaGFzT3duUHJvcGVydHkuY2FsbChiLCBwKSkgZFtwXSA9IGJbcF07XG4gICAgfTtcbiAgICByZXR1cm4gZXh0ZW5kU3RhdGljcyhkLCBiKTtcbiAgfTtcbiAgcmV0dXJuIGZ1bmN0aW9uIChkLCBiKSB7XG4gICAgaWYgKHR5cGVvZiBiICE9PSBcImZ1bmN0aW9uXCIgJiYgYiAhPT0gbnVsbCkgdGhyb3cgbmV3IFR5cGVFcnJvcihcIkNsYXNzIGV4dGVuZHMgdmFsdWUgXCIgKyBTdHJpbmcoYikgKyBcIiBpcyBub3QgYSBjb25zdHJ1Y3RvciBvciBudWxsXCIpO1xuICAgIGV4dGVuZFN0YXRpY3MoZCwgYik7XG4gICAgZnVuY3Rpb24gX18oKSB7XG4gICAgICB0aGlzLmNvbnN0cnVjdG9yID0gZDtcbiAgICB9XG4gICAgZC5wcm90b3R5cGUgPSBiID09PSBudWxsID8gT2JqZWN0LmNyZWF0ZShiKSA6IChfXy5wcm90b3R5cGUgPSBiLnByb3RvdHlwZSwgbmV3IF9fKCkpO1xuICB9O1xufSgpO1xudmFyIF9fcmVhZCA9IHRoaXMgJiYgdGhpcy5fX3JlYWQgfHwgZnVuY3Rpb24gKG8sIG4pIHtcbiAgdmFyIG0gPSB0eXBlb2YgU3ltYm9sID09PSBcImZ1bmN0aW9uXCIgJiYgb1tTeW1ib2wuaXRlcmF0b3JdO1xuICBpZiAoIW0pIHJldHVybiBvO1xuICB2YXIgaSA9IG0uY2FsbChvKSxcbiAgICByLFxuICAgIGFyID0gW10sXG4gICAgZTtcbiAgdHJ5IHtcbiAgICB3aGlsZSAoKG4gPT09IHZvaWQgMCB8fCBuLS0gPiAwKSAmJiAhKHIgPSBpLm5leHQoKSkuZG9uZSkgYXIucHVzaChyLnZhbHVlKTtcbiAgfSBjYXRjaCAoZXJyb3IpIHtcbiAgICBlID0ge1xuICAgICAgZXJyb3I6IGVycm9yXG4gICAgfTtcbiAgfSBmaW5hbGx5IHtcbiAgICB0cnkge1xuICAgICAgaWYgKHIgJiYgIXIuZG9uZSAmJiAobSA9IGlbXCJyZXR1cm5cIl0pKSBtLmNhbGwoaSk7XG4gICAgfSBmaW5hbGx5IHtcbiAgICAgIGlmIChlKSB0aHJvdyBlLmVycm9yO1xuICAgIH1cbiAgfVxuICByZXR1cm4gYXI7XG59O1xuT2JqZWN0LmRlZmluZVByb3BlcnR5KGV4cG9ydHMsIFwiX19lc01vZHVsZVwiLCB7XG4gIHZhbHVlOiB0cnVlXG59KTtcbmV4cG9ydHMuRmluZFRlWCA9IHZvaWQgMDtcbnZhciBGaW5kTWF0aF9qc18xID0gcmVxdWlyZShcIi4uLy4uL2NvcmUvRmluZE1hdGguanNcIik7XG52YXIgc3RyaW5nX2pzXzEgPSByZXF1aXJlKFwiLi4vLi4vdXRpbC9zdHJpbmcuanNcIik7XG52YXIgTWF0aEl0ZW1fanNfMSA9IHJlcXVpcmUoXCIuLi8uLi9jb3JlL01hdGhJdGVtLmpzXCIpO1xudmFyIEZpbmRUZVggPSBmdW5jdGlvbiAoX3N1cGVyKSB7XG4gIF9fZXh0ZW5kcyhGaW5kVGVYLCBfc3VwZXIpO1xuICBmdW5jdGlvbiBGaW5kVGVYKG9wdGlvbnMpIHtcbiAgICB2YXIgX3RoaXMgPSBfc3VwZXIuY2FsbCh0aGlzLCBvcHRpb25zKSB8fCB0aGlzO1xuICAgIF90aGlzLmdldFBhdHRlcm5zKCk7XG4gICAgcmV0dXJuIF90aGlzO1xuICB9XG4gIEZpbmRUZVgucHJvdG90eXBlLmdldFBhdHRlcm5zID0gZnVuY3Rpb24gKCkge1xuICAgIHZhciBfdGhpcyA9IHRoaXM7XG4gICAgdmFyIG9wdGlvbnMgPSB0aGlzLm9wdGlvbnM7XG4gICAgdmFyIHN0YXJ0cyA9IFtdLFxuICAgICAgcGFydHMgPSBbXSxcbiAgICAgIHN1YnBhcnRzID0gW107XG4gICAgdGhpcy5lbmQgPSB7fTtcbiAgICB0aGlzLmVudiA9IHRoaXMuc3ViID0gMDtcbiAgICB2YXIgaSA9IDE7XG4gICAgb3B0aW9uc1snaW5saW5lTWF0aCddLmZvckVhY2goZnVuY3Rpb24gKGRlbGltcykge1xuICAgICAgcmV0dXJuIF90aGlzLmFkZFBhdHRlcm4oc3RhcnRzLCBkZWxpbXMsIGZhbHNlKTtcbiAgICB9KTtcbiAgICBvcHRpb25zWydkaXNwbGF5TWF0aCddLmZvckVhY2goZnVuY3Rpb24gKGRlbGltcykge1xuICAgICAgcmV0dXJuIF90aGlzLmFkZFBhdHRlcm4oc3RhcnRzLCBkZWxpbXMsIHRydWUpO1xuICAgIH0pO1xuICAgIGlmIChzdGFydHMubGVuZ3RoKSB7XG4gICAgICBwYXJ0cy5wdXNoKHN0YXJ0cy5zb3J0KHN0cmluZ19qc18xLnNvcnRMZW5ndGgpLmpvaW4oJ3wnKSk7XG4gICAgfVxuICAgIGlmIChvcHRpb25zWydwcm9jZXNzRW52aXJvbm1lbnRzJ10pIHtcbiAgICAgIHBhcnRzLnB1c2goJ1xcXFxcXFxcYmVnaW5cXFxccypcXFxceyhbXn1dKilcXFxcfScpO1xuICAgICAgdGhpcy5lbnYgPSBpO1xuICAgICAgaSsrO1xuICAgIH1cbiAgICBpZiAob3B0aW9uc1sncHJvY2Vzc0VzY2FwZXMnXSkge1xuICAgICAgc3VicGFydHMucHVzaCgnXFxcXFxcXFwoW1xcXFxcXFxcJF0pJyk7XG4gICAgfVxuICAgIGlmIChvcHRpb25zWydwcm9jZXNzUmVmcyddKSB7XG4gICAgICBzdWJwYXJ0cy5wdXNoKCcoXFxcXFxcXFwoPzplcSk/cmVmXFxcXHMqXFxcXHtbXn1dKlxcXFx9KScpO1xuICAgIH1cbiAgICBpZiAoc3VicGFydHMubGVuZ3RoKSB7XG4gICAgICBwYXJ0cy5wdXNoKCcoJyArIHN1YnBhcnRzLmpvaW4oJ3wnKSArICcpJyk7XG4gICAgICB0aGlzLnN1YiA9IGk7XG4gICAgfVxuICAgIHRoaXMuc3RhcnQgPSBuZXcgUmVnRXhwKHBhcnRzLmpvaW4oJ3wnKSwgJ2cnKTtcbiAgICB0aGlzLmhhc1BhdHRlcm5zID0gcGFydHMubGVuZ3RoID4gMDtcbiAgfTtcbiAgRmluZFRlWC5wcm90b3R5cGUuYWRkUGF0dGVybiA9IGZ1bmN0aW9uIChzdGFydHMsIGRlbGltcywgZGlzcGxheSkge1xuICAgIHZhciBfYSA9IF9fcmVhZChkZWxpbXMsIDIpLFxuICAgICAgb3BlbiA9IF9hWzBdLFxuICAgICAgY2xvc2UgPSBfYVsxXTtcbiAgICBzdGFydHMucHVzaCgoMCwgc3RyaW5nX2pzXzEucXVvdGVQYXR0ZXJuKShvcGVuKSk7XG4gICAgdGhpcy5lbmRbb3Blbl0gPSBbY2xvc2UsIGRpc3BsYXksIHRoaXMuZW5kUGF0dGVybihjbG9zZSldO1xuICB9O1xuICBGaW5kVGVYLnByb3RvdHlwZS5lbmRQYXR0ZXJuID0gZnVuY3Rpb24gKGVuZCwgZW5kcCkge1xuICAgIHJldHVybiBuZXcgUmVnRXhwKChlbmRwIHx8ICgwLCBzdHJpbmdfanNfMS5xdW90ZVBhdHRlcm4pKGVuZCkpICsgJ3xcXFxcXFxcXCg/OlthLXpBLVpdfC4pfFt7fV0nLCAnZycpO1xuICB9O1xuICBGaW5kVGVYLnByb3RvdHlwZS5maW5kRW5kID0gZnVuY3Rpb24gKHRleHQsIG4sIHN0YXJ0LCBlbmQpIHtcbiAgICB2YXIgX2EgPSBfX3JlYWQoZW5kLCAzKSxcbiAgICAgIGNsb3NlID0gX2FbMF0sXG4gICAgICBkaXNwbGF5ID0gX2FbMV0sXG4gICAgICBwYXR0ZXJuID0gX2FbMl07XG4gICAgdmFyIGkgPSBwYXR0ZXJuLmxhc3RJbmRleCA9IHN0YXJ0LmluZGV4ICsgc3RhcnRbMF0ubGVuZ3RoO1xuICAgIHZhciBtYXRjaCxcbiAgICAgIGJyYWNlcyA9IDA7XG4gICAgd2hpbGUgKG1hdGNoID0gcGF0dGVybi5leGVjKHRleHQpKSB7XG4gICAgICBpZiAoKG1hdGNoWzFdIHx8IG1hdGNoWzBdKSA9PT0gY2xvc2UgJiYgYnJhY2VzID09PSAwKSB7XG4gICAgICAgIHJldHVybiAoMCwgTWF0aEl0ZW1fanNfMS5wcm90b0l0ZW0pKHN0YXJ0WzBdLCB0ZXh0LnN1YnN0cihpLCBtYXRjaC5pbmRleCAtIGkpLCBtYXRjaFswXSwgbiwgc3RhcnQuaW5kZXgsIG1hdGNoLmluZGV4ICsgbWF0Y2hbMF0ubGVuZ3RoLCBkaXNwbGF5KTtcbiAgICAgIH0gZWxzZSBpZiAobWF0Y2hbMF0gPT09ICd7Jykge1xuICAgICAgICBicmFjZXMrKztcbiAgICAgIH0gZWxzZSBpZiAobWF0Y2hbMF0gPT09ICd9JyAmJiBicmFjZXMpIHtcbiAgICAgICAgYnJhY2VzLS07XG4gICAgICB9XG4gICAgfVxuICAgIHJldHVybiBudWxsO1xuICB9O1xuICBGaW5kVGVYLnByb3RvdHlwZS5maW5kTWF0aEluU3RyaW5nID0gZnVuY3Rpb24gKG1hdGgsIG4sIHRleHQpIHtcbiAgICB2YXIgc3RhcnQsIG1hdGNoO1xuICAgIHRoaXMuc3RhcnQubGFzdEluZGV4ID0gMDtcbiAgICB3aGlsZSAoc3RhcnQgPSB0aGlzLnN0YXJ0LmV4ZWModGV4dCkpIHtcbiAgICAgIGlmIChzdGFydFt0aGlzLmVudl0gIT09IHVuZGVmaW5lZCAmJiB0aGlzLmVudikge1xuICAgICAgICB2YXIgZW5kID0gJ1xcXFxcXFxcZW5kXFxcXHMqKFxcXFx7JyArICgwLCBzdHJpbmdfanNfMS5xdW90ZVBhdHRlcm4pKHN0YXJ0W3RoaXMuZW52XSkgKyAnXFxcXH0pJztcbiAgICAgICAgbWF0Y2ggPSB0aGlzLmZpbmRFbmQodGV4dCwgbiwgc3RhcnQsIFsneycgKyBzdGFydFt0aGlzLmVudl0gKyAnfScsIHRydWUsIHRoaXMuZW5kUGF0dGVybihudWxsLCBlbmQpXSk7XG4gICAgICAgIGlmIChtYXRjaCkge1xuICAgICAgICAgIG1hdGNoLm1hdGggPSBtYXRjaC5vcGVuICsgbWF0Y2gubWF0aCArIG1hdGNoLmNsb3NlO1xuICAgICAgICAgIG1hdGNoLm9wZW4gPSBtYXRjaC5jbG9zZSA9ICcnO1xuICAgICAgICB9XG4gICAgICB9IGVsc2UgaWYgKHN0YXJ0W3RoaXMuc3ViXSAhPT0gdW5kZWZpbmVkICYmIHRoaXMuc3ViKSB7XG4gICAgICAgIHZhciBtYXRoXzEgPSBzdGFydFt0aGlzLnN1Yl07XG4gICAgICAgIHZhciBlbmQgPSBzdGFydC5pbmRleCArIHN0YXJ0W3RoaXMuc3ViXS5sZW5ndGg7XG4gICAgICAgIGlmIChtYXRoXzEubGVuZ3RoID09PSAyKSB7XG4gICAgICAgICAgbWF0Y2ggPSAoMCwgTWF0aEl0ZW1fanNfMS5wcm90b0l0ZW0pKCcnLCBtYXRoXzEuc3Vic3RyKDEpLCAnJywgbiwgc3RhcnQuaW5kZXgsIGVuZCk7XG4gICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgbWF0Y2ggPSAoMCwgTWF0aEl0ZW1fanNfMS5wcm90b0l0ZW0pKCcnLCBtYXRoXzEsICcnLCBuLCBzdGFydC5pbmRleCwgZW5kLCBmYWxzZSk7XG4gICAgICAgIH1cbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIG1hdGNoID0gdGhpcy5maW5kRW5kKHRleHQsIG4sIHN0YXJ0LCB0aGlzLmVuZFtzdGFydFswXV0pO1xuICAgICAgfVxuICAgICAgaWYgKG1hdGNoKSB7XG4gICAgICAgIG1hdGgucHVzaChtYXRjaCk7XG4gICAgICAgIHRoaXMuc3RhcnQubGFzdEluZGV4ID0gbWF0Y2guZW5kLm47XG4gICAgICB9XG4gICAgfVxuICB9O1xuICBGaW5kVGVYLnByb3RvdHlwZS5maW5kTWF0aCA9IGZ1bmN0aW9uIChzdHJpbmdzKSB7XG4gICAgdmFyIG1hdGggPSBbXTtcbiAgICBpZiAodGhpcy5oYXNQYXR0ZXJucykge1xuICAgICAgZm9yICh2YXIgaSA9IDAsIG0gPSBzdHJpbmdzLmxlbmd0aDsgaSA8IG07IGkrKykge1xuICAgICAgICB0aGlzLmZpbmRNYXRoSW5TdHJpbmcobWF0aCwgaSwgc3RyaW5nc1tpXSk7XG4gICAgICB9XG4gICAgfVxuICAgIHJldHVybiBtYXRoO1xuICB9O1xuICBGaW5kVGVYLk9QVElPTlMgPSB7XG4gICAgaW5saW5lTWF0aDogW1snXFxcXCgnLCAnXFxcXCknXV0sXG4gICAgZGlzcGxheU1hdGg6IFtbJyQkJywgJyQkJ10sIFsnXFxcXFsnLCAnXFxcXF0nXV0sXG4gICAgcHJvY2Vzc0VzY2FwZXM6IHRydWUsXG4gICAgcHJvY2Vzc0Vudmlyb25tZW50czogdHJ1ZSxcbiAgICBwcm9jZXNzUmVmczogdHJ1ZVxuICB9O1xuICByZXR1cm4gRmluZFRlWDtcbn0oRmluZE1hdGhfanNfMS5BYnN0cmFjdEZpbmRNYXRoKTtcbmV4cG9ydHMuRmluZFRlWCA9IEZpbmRUZVg7Il0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9
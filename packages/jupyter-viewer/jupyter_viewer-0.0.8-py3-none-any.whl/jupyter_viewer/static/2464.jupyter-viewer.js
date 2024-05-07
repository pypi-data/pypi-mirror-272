"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[2464],{

/***/ 9312:
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
Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports.AbstractHandler = void 0;
var MathDocument_js_1 = __webpack_require__(85520);
var DefaultMathDocument = function (_super) {
  __extends(DefaultMathDocument, _super);
  function DefaultMathDocument() {
    return _super !== null && _super.apply(this, arguments) || this;
  }
  return DefaultMathDocument;
}(MathDocument_js_1.AbstractMathDocument);
var AbstractHandler = function () {
  function AbstractHandler(adaptor, priority) {
    if (priority === void 0) {
      priority = 5;
    }
    this.documentClass = DefaultMathDocument;
    this.adaptor = adaptor;
    this.priority = priority;
  }
  Object.defineProperty(AbstractHandler.prototype, "name", {
    get: function () {
      return this.constructor.NAME;
    },
    enumerable: false,
    configurable: true
  });
  AbstractHandler.prototype.handlesDocument = function (_document) {
    return false;
  };
  AbstractHandler.prototype.create = function (document, options) {
    return new this.documentClass(document, this.adaptor, options);
  };
  AbstractHandler.NAME = 'generic';
  return AbstractHandler;
}();
exports.AbstractHandler = AbstractHandler;

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

/***/ 85520:
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
exports.AbstractMathDocument = exports.resetAllOptions = exports.resetOptions = exports.RenderList = void 0;
var Options_js_1 = __webpack_require__(62704);
var InputJax_js_1 = __webpack_require__(87261);
var OutputJax_js_1 = __webpack_require__(63914);
var MathList_js_1 = __webpack_require__(82433);
var MathItem_js_1 = __webpack_require__(57714);
var MmlFactory_js_1 = __webpack_require__(77208);
var BitField_js_1 = __webpack_require__(37367);
var PrioritizedList_js_1 = __webpack_require__(47144);
var RenderList = function (_super) {
  __extends(RenderList, _super);
  function RenderList() {
    return _super !== null && _super.apply(this, arguments) || this;
  }
  RenderList.create = function (actions) {
    var e_1, _a;
    var list = new this();
    try {
      for (var _b = __values(Object.keys(actions)), _c = _b.next(); !_c.done; _c = _b.next()) {
        var id = _c.value;
        var _d = __read(this.action(id, actions[id]), 2),
          action = _d[0],
          priority = _d[1];
        if (priority) {
          list.add(action, priority);
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
    return list;
  };
  RenderList.action = function (id, action) {
    var _a, _b, _c, _d;
    var renderDoc, renderMath;
    var convert = true;
    var priority = action[0];
    if (action.length === 1 || typeof action[1] === 'boolean') {
      action.length === 2 && (convert = action[1]);
      _a = __read(this.methodActions(id), 2), renderDoc = _a[0], renderMath = _a[1];
    } else if (typeof action[1] === 'string') {
      if (typeof action[2] === 'string') {
        action.length === 4 && (convert = action[3]);
        var _e = __read(action.slice(1), 2),
          method1 = _e[0],
          method2 = _e[1];
        _b = __read(this.methodActions(method1, method2), 2), renderDoc = _b[0], renderMath = _b[1];
      } else {
        action.length === 3 && (convert = action[2]);
        _c = __read(this.methodActions(action[1]), 2), renderDoc = _c[0], renderMath = _c[1];
      }
    } else {
      action.length === 4 && (convert = action[3]);
      _d = __read(action.slice(1), 2), renderDoc = _d[0], renderMath = _d[1];
    }
    return [{
      id: id,
      renderDoc: renderDoc,
      renderMath: renderMath,
      convert: convert
    }, priority];
  };
  RenderList.methodActions = function (method1, method2) {
    if (method2 === void 0) {
      method2 = method1;
    }
    return [function (document) {
      method1 && document[method1]();
      return false;
    }, function (math, document) {
      method2 && math[method2](document);
      return false;
    }];
  };
  RenderList.prototype.renderDoc = function (document, start) {
    var e_2, _a;
    if (start === void 0) {
      start = MathItem_js_1.STATE.UNPROCESSED;
    }
    try {
      for (var _b = __values(this.items), _c = _b.next(); !_c.done; _c = _b.next()) {
        var item = _c.value;
        if (item.priority >= start) {
          if (item.item.renderDoc(document)) return;
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
  };
  RenderList.prototype.renderMath = function (math, document, start) {
    var e_3, _a;
    if (start === void 0) {
      start = MathItem_js_1.STATE.UNPROCESSED;
    }
    try {
      for (var _b = __values(this.items), _c = _b.next(); !_c.done; _c = _b.next()) {
        var item = _c.value;
        if (item.priority >= start) {
          if (item.item.renderMath(math, document)) return;
        }
      }
    } catch (e_3_1) {
      e_3 = {
        error: e_3_1
      };
    } finally {
      try {
        if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
      } finally {
        if (e_3) throw e_3.error;
      }
    }
  };
  RenderList.prototype.renderConvert = function (math, document, end) {
    var e_4, _a;
    if (end === void 0) {
      end = MathItem_js_1.STATE.LAST;
    }
    try {
      for (var _b = __values(this.items), _c = _b.next(); !_c.done; _c = _b.next()) {
        var item = _c.value;
        if (item.priority > end) return;
        if (item.item.convert) {
          if (item.item.renderMath(math, document)) return;
        }
      }
    } catch (e_4_1) {
      e_4 = {
        error: e_4_1
      };
    } finally {
      try {
        if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
      } finally {
        if (e_4) throw e_4.error;
      }
    }
  };
  RenderList.prototype.findID = function (id) {
    var e_5, _a;
    try {
      for (var _b = __values(this.items), _c = _b.next(); !_c.done; _c = _b.next()) {
        var item = _c.value;
        if (item.item.id === id) {
          return item.item;
        }
      }
    } catch (e_5_1) {
      e_5 = {
        error: e_5_1
      };
    } finally {
      try {
        if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
      } finally {
        if (e_5) throw e_5.error;
      }
    }
    return null;
  };
  return RenderList;
}(PrioritizedList_js_1.PrioritizedList);
exports.RenderList = RenderList;
exports.resetOptions = {
  all: false,
  processed: false,
  inputJax: null,
  outputJax: null
};
exports.resetAllOptions = {
  all: true,
  processed: true,
  inputJax: [],
  outputJax: []
};
var DefaultInputJax = function (_super) {
  __extends(DefaultInputJax, _super);
  function DefaultInputJax() {
    return _super !== null && _super.apply(this, arguments) || this;
  }
  DefaultInputJax.prototype.compile = function (_math) {
    return null;
  };
  return DefaultInputJax;
}(InputJax_js_1.AbstractInputJax);
var DefaultOutputJax = function (_super) {
  __extends(DefaultOutputJax, _super);
  function DefaultOutputJax() {
    return _super !== null && _super.apply(this, arguments) || this;
  }
  DefaultOutputJax.prototype.typeset = function (_math, _document) {
    if (_document === void 0) {
      _document = null;
    }
    return null;
  };
  DefaultOutputJax.prototype.escaped = function (_math, _document) {
    return null;
  };
  return DefaultOutputJax;
}(OutputJax_js_1.AbstractOutputJax);
var DefaultMathList = function (_super) {
  __extends(DefaultMathList, _super);
  function DefaultMathList() {
    return _super !== null && _super.apply(this, arguments) || this;
  }
  return DefaultMathList;
}(MathList_js_1.AbstractMathList);
var DefaultMathItem = function (_super) {
  __extends(DefaultMathItem, _super);
  function DefaultMathItem() {
    return _super !== null && _super.apply(this, arguments) || this;
  }
  return DefaultMathItem;
}(MathItem_js_1.AbstractMathItem);
var AbstractMathDocument = function () {
  function AbstractMathDocument(document, adaptor, options) {
    var _this = this;
    var CLASS = this.constructor;
    this.document = document;
    this.options = (0, Options_js_1.userOptions)((0, Options_js_1.defaultOptions)({}, CLASS.OPTIONS), options);
    this.math = new (this.options['MathList'] || DefaultMathList)();
    this.renderActions = RenderList.create(this.options['renderActions']);
    this.processed = new AbstractMathDocument.ProcessBits();
    this.outputJax = this.options['OutputJax'] || new DefaultOutputJax();
    var inputJax = this.options['InputJax'] || [new DefaultInputJax()];
    if (!Array.isArray(inputJax)) {
      inputJax = [inputJax];
    }
    this.inputJax = inputJax;
    this.adaptor = adaptor;
    this.outputJax.setAdaptor(adaptor);
    this.inputJax.map(function (jax) {
      return jax.setAdaptor(adaptor);
    });
    this.mmlFactory = this.options['MmlFactory'] || new MmlFactory_js_1.MmlFactory();
    this.inputJax.map(function (jax) {
      return jax.setMmlFactory(_this.mmlFactory);
    });
    this.outputJax.initialize();
    this.inputJax.map(function (jax) {
      return jax.initialize();
    });
  }
  Object.defineProperty(AbstractMathDocument.prototype, "kind", {
    get: function () {
      return this.constructor.KIND;
    },
    enumerable: false,
    configurable: true
  });
  AbstractMathDocument.prototype.addRenderAction = function (id) {
    var action = [];
    for (var _i = 1; _i < arguments.length; _i++) {
      action[_i - 1] = arguments[_i];
    }
    var _a = __read(RenderList.action(id, action), 2),
      fn = _a[0],
      p = _a[1];
    this.renderActions.add(fn, p);
  };
  AbstractMathDocument.prototype.removeRenderAction = function (id) {
    var action = this.renderActions.findID(id);
    if (action) {
      this.renderActions.remove(action);
    }
  };
  AbstractMathDocument.prototype.render = function () {
    this.renderActions.renderDoc(this);
    return this;
  };
  AbstractMathDocument.prototype.rerender = function (start) {
    if (start === void 0) {
      start = MathItem_js_1.STATE.RERENDER;
    }
    this.state(start - 1);
    this.render();
    return this;
  };
  AbstractMathDocument.prototype.convert = function (math, options) {
    if (options === void 0) {
      options = {};
    }
    var _a = (0, Options_js_1.userOptions)({
        format: this.inputJax[0].name,
        display: true,
        end: MathItem_js_1.STATE.LAST,
        em: 16,
        ex: 8,
        containerWidth: null,
        lineWidth: 1000000,
        scale: 1,
        family: ''
      }, options),
      format = _a.format,
      display = _a.display,
      end = _a.end,
      ex = _a.ex,
      em = _a.em,
      containerWidth = _a.containerWidth,
      lineWidth = _a.lineWidth,
      scale = _a.scale,
      family = _a.family;
    if (containerWidth === null) {
      containerWidth = 80 * ex;
    }
    var jax = this.inputJax.reduce(function (jax, ijax) {
      return ijax.name === format ? ijax : jax;
    }, null);
    var mitem = new this.options.MathItem(math, jax, display);
    mitem.start.node = this.adaptor.body(this.document);
    mitem.setMetrics(em, ex, containerWidth, lineWidth, scale);
    if (this.outputJax.options.mtextInheritFont) {
      mitem.outputData.mtextFamily = family;
    }
    if (this.outputJax.options.merrorInheritFont) {
      mitem.outputData.merrorFamily = family;
    }
    mitem.convert(this, end);
    return mitem.typesetRoot || mitem.root;
  };
  AbstractMathDocument.prototype.findMath = function (_options) {
    if (_options === void 0) {
      _options = null;
    }
    this.processed.set('findMath');
    return this;
  };
  AbstractMathDocument.prototype.compile = function () {
    var e_6, _a, e_7, _b;
    if (!this.processed.isSet('compile')) {
      var recompile = [];
      try {
        for (var _c = __values(this.math), _d = _c.next(); !_d.done; _d = _c.next()) {
          var math = _d.value;
          this.compileMath(math);
          if (math.inputData.recompile !== undefined) {
            recompile.push(math);
          }
        }
      } catch (e_6_1) {
        e_6 = {
          error: e_6_1
        };
      } finally {
        try {
          if (_d && !_d.done && (_a = _c.return)) _a.call(_c);
        } finally {
          if (e_6) throw e_6.error;
        }
      }
      try {
        for (var recompile_1 = __values(recompile), recompile_1_1 = recompile_1.next(); !recompile_1_1.done; recompile_1_1 = recompile_1.next()) {
          var math = recompile_1_1.value;
          var data = math.inputData.recompile;
          math.state(data.state);
          math.inputData.recompile = data;
          this.compileMath(math);
        }
      } catch (e_7_1) {
        e_7 = {
          error: e_7_1
        };
      } finally {
        try {
          if (recompile_1_1 && !recompile_1_1.done && (_b = recompile_1.return)) _b.call(recompile_1);
        } finally {
          if (e_7) throw e_7.error;
        }
      }
      this.processed.set('compile');
    }
    return this;
  };
  AbstractMathDocument.prototype.compileMath = function (math) {
    try {
      math.compile(this);
    } catch (err) {
      if (err.retry || err.restart) {
        throw err;
      }
      this.options['compileError'](this, math, err);
      math.inputData['error'] = err;
    }
  };
  AbstractMathDocument.prototype.compileError = function (math, err) {
    math.root = this.mmlFactory.create('math', null, [this.mmlFactory.create('merror', {
      'data-mjx-error': err.message,
      title: err.message
    }, [this.mmlFactory.create('mtext', null, [this.mmlFactory.create('text').setText('Math input error')])])]);
    if (math.display) {
      math.root.attributes.set('display', 'block');
    }
    math.inputData.error = err.message;
  };
  AbstractMathDocument.prototype.typeset = function () {
    var e_8, _a;
    if (!this.processed.isSet('typeset')) {
      try {
        for (var _b = __values(this.math), _c = _b.next(); !_c.done; _c = _b.next()) {
          var math = _c.value;
          try {
            math.typeset(this);
          } catch (err) {
            if (err.retry || err.restart) {
              throw err;
            }
            this.options['typesetError'](this, math, err);
            math.outputData['error'] = err;
          }
        }
      } catch (e_8_1) {
        e_8 = {
          error: e_8_1
        };
      } finally {
        try {
          if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
        } finally {
          if (e_8) throw e_8.error;
        }
      }
      this.processed.set('typeset');
    }
    return this;
  };
  AbstractMathDocument.prototype.typesetError = function (math, err) {
    math.typesetRoot = this.adaptor.node('mjx-container', {
      class: 'MathJax mjx-output-error',
      jax: this.outputJax.name
    }, [this.adaptor.node('span', {
      'data-mjx-error': err.message,
      title: err.message,
      style: {
        color: 'red',
        'background-color': 'yellow',
        'line-height': 'normal'
      }
    }, [this.adaptor.text('Math output error')])]);
    if (math.display) {
      this.adaptor.setAttributes(math.typesetRoot, {
        style: {
          display: 'block',
          margin: '1em 0',
          'text-align': 'center'
        }
      });
    }
    math.outputData.error = err.message;
  };
  AbstractMathDocument.prototype.getMetrics = function () {
    if (!this.processed.isSet('getMetrics')) {
      this.outputJax.getMetrics(this);
      this.processed.set('getMetrics');
    }
    return this;
  };
  AbstractMathDocument.prototype.updateDocument = function () {
    var e_9, _a;
    if (!this.processed.isSet('updateDocument')) {
      try {
        for (var _b = __values(this.math.reversed()), _c = _b.next(); !_c.done; _c = _b.next()) {
          var math = _c.value;
          math.updateDocument(this);
        }
      } catch (e_9_1) {
        e_9 = {
          error: e_9_1
        };
      } finally {
        try {
          if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
        } finally {
          if (e_9) throw e_9.error;
        }
      }
      this.processed.set('updateDocument');
    }
    return this;
  };
  AbstractMathDocument.prototype.removeFromDocument = function (_restore) {
    if (_restore === void 0) {
      _restore = false;
    }
    return this;
  };
  AbstractMathDocument.prototype.state = function (state, restore) {
    var e_10, _a;
    if (restore === void 0) {
      restore = false;
    }
    try {
      for (var _b = __values(this.math), _c = _b.next(); !_c.done; _c = _b.next()) {
        var math = _c.value;
        math.state(state, restore);
      }
    } catch (e_10_1) {
      e_10 = {
        error: e_10_1
      };
    } finally {
      try {
        if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
      } finally {
        if (e_10) throw e_10.error;
      }
    }
    if (state < MathItem_js_1.STATE.INSERTED) {
      this.processed.clear('updateDocument');
    }
    if (state < MathItem_js_1.STATE.TYPESET) {
      this.processed.clear('typeset');
      this.processed.clear('getMetrics');
    }
    if (state < MathItem_js_1.STATE.COMPILED) {
      this.processed.clear('compile');
    }
    return this;
  };
  AbstractMathDocument.prototype.reset = function (options) {
    var _a;
    if (options === void 0) {
      options = {
        processed: true
      };
    }
    options = (0, Options_js_1.userOptions)(Object.assign({}, exports.resetOptions), options);
    options.all && Object.assign(options, exports.resetAllOptions);
    options.processed && this.processed.reset();
    options.inputJax && this.inputJax.forEach(function (jax) {
      return jax.reset.apply(jax, __spreadArray([], __read(options.inputJax), false));
    });
    options.outputJax && (_a = this.outputJax).reset.apply(_a, __spreadArray([], __read(options.outputJax), false));
    return this;
  };
  AbstractMathDocument.prototype.clear = function () {
    this.reset();
    this.math.clear();
    return this;
  };
  AbstractMathDocument.prototype.concat = function (list) {
    this.math.merge(list);
    return this;
  };
  AbstractMathDocument.prototype.clearMathItemsWithin = function (containers) {
    var _a;
    var items = this.getMathItemsWithin(containers);
    (_a = this.math).remove.apply(_a, __spreadArray([], __read(items), false));
    return items;
  };
  AbstractMathDocument.prototype.getMathItemsWithin = function (elements) {
    var e_11, _a, e_12, _b;
    if (!Array.isArray(elements)) {
      elements = [elements];
    }
    var adaptor = this.adaptor;
    var items = [];
    var containers = adaptor.getElements(elements, this.document);
    try {
      ITEMS: for (var _c = __values(this.math), _d = _c.next(); !_d.done; _d = _c.next()) {
        var item = _d.value;
        try {
          for (var containers_1 = (e_12 = void 0, __values(containers)), containers_1_1 = containers_1.next(); !containers_1_1.done; containers_1_1 = containers_1.next()) {
            var container = containers_1_1.value;
            if (item.start.node && adaptor.contains(container, item.start.node)) {
              items.push(item);
              continue ITEMS;
            }
          }
        } catch (e_12_1) {
          e_12 = {
            error: e_12_1
          };
        } finally {
          try {
            if (containers_1_1 && !containers_1_1.done && (_b = containers_1.return)) _b.call(containers_1);
          } finally {
            if (e_12) throw e_12.error;
          }
        }
      }
    } catch (e_11_1) {
      e_11 = {
        error: e_11_1
      };
    } finally {
      try {
        if (_d && !_d.done && (_a = _c.return)) _a.call(_c);
      } finally {
        if (e_11) throw e_11.error;
      }
    }
    return items;
  };
  AbstractMathDocument.KIND = 'MathDocument';
  AbstractMathDocument.OPTIONS = {
    OutputJax: null,
    InputJax: null,
    MmlFactory: null,
    MathList: DefaultMathList,
    MathItem: DefaultMathItem,
    compileError: function (doc, math, err) {
      doc.compileError(math, err);
    },
    typesetError: function (doc, math, err) {
      doc.typesetError(math, err);
    },
    renderActions: (0, Options_js_1.expandable)({
      find: [MathItem_js_1.STATE.FINDMATH, 'findMath', '', false],
      compile: [MathItem_js_1.STATE.COMPILED],
      metrics: [MathItem_js_1.STATE.METRICS, 'getMetrics', '', false],
      typeset: [MathItem_js_1.STATE.TYPESET],
      update: [MathItem_js_1.STATE.INSERTED, 'updateDocument', false]
    })
  };
  AbstractMathDocument.ProcessBits = (0, BitField_js_1.BitFieldClass)('findMath', 'compile', 'getMetrics', 'typeset', 'updateDocument');
  return AbstractMathDocument;
}();
exports.AbstractMathDocument = AbstractMathDocument;

/***/ }),

/***/ 82433:
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
Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports.AbstractMathList = void 0;
var LinkedList_js_1 = __webpack_require__(4717);
var AbstractMathList = function (_super) {
  __extends(AbstractMathList, _super);
  function AbstractMathList() {
    return _super !== null && _super.apply(this, arguments) || this;
  }
  AbstractMathList.prototype.isBefore = function (a, b) {
    return a.start.i < b.start.i || a.start.i === b.start.i && a.start.n < b.start.n;
  };
  return AbstractMathList;
}(LinkedList_js_1.LinkedList);
exports.AbstractMathList = AbstractMathList;

/***/ }),

/***/ 63914:
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {



Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports.AbstractOutputJax = void 0;
var Options_js_1 = __webpack_require__(62704);
var FunctionList_js_1 = __webpack_require__(58235);
var AbstractOutputJax = function () {
  function AbstractOutputJax(options) {
    if (options === void 0) {
      options = {};
    }
    this.adaptor = null;
    var CLASS = this.constructor;
    this.options = (0, Options_js_1.userOptions)((0, Options_js_1.defaultOptions)({}, CLASS.OPTIONS), options);
    this.postFilters = new FunctionList_js_1.FunctionList();
  }
  Object.defineProperty(AbstractOutputJax.prototype, "name", {
    get: function () {
      return this.constructor.NAME;
    },
    enumerable: false,
    configurable: true
  });
  AbstractOutputJax.prototype.setAdaptor = function (adaptor) {
    this.adaptor = adaptor;
  };
  AbstractOutputJax.prototype.initialize = function () {};
  AbstractOutputJax.prototype.reset = function () {
    var _args = [];
    for (var _i = 0; _i < arguments.length; _i++) {
      _args[_i] = arguments[_i];
    }
  };
  AbstractOutputJax.prototype.getMetrics = function (_document) {};
  AbstractOutputJax.prototype.styleSheet = function (_document) {
    return null;
  };
  AbstractOutputJax.prototype.pageElements = function (_document) {
    return null;
  };
  AbstractOutputJax.prototype.executeFilters = function (filters, math, document, data) {
    var args = {
      math: math,
      document: document,
      data: data
    };
    filters.execute(args);
    return args.data;
  };
  AbstractOutputJax.NAME = 'generic';
  AbstractOutputJax.OPTIONS = {};
  return AbstractOutputJax;
}();
exports.AbstractOutputJax = AbstractOutputJax;

/***/ }),

/***/ 98435:
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
exports.HTMLDocument = void 0;
var MathDocument_js_1 = __webpack_require__(85520);
var Options_js_1 = __webpack_require__(62704);
var HTMLMathItem_js_1 = __webpack_require__(92223);
var HTMLMathList_js_1 = __webpack_require__(99432);
var HTMLDomStrings_js_1 = __webpack_require__(84915);
var MathItem_js_1 = __webpack_require__(57714);
var HTMLDocument = function (_super) {
  __extends(HTMLDocument, _super);
  function HTMLDocument(document, adaptor, options) {
    var _this = this;
    var _a = __read((0, Options_js_1.separateOptions)(options, HTMLDomStrings_js_1.HTMLDomStrings.OPTIONS), 2),
      html = _a[0],
      dom = _a[1];
    _this = _super.call(this, document, adaptor, html) || this;
    _this.domStrings = _this.options['DomStrings'] || new HTMLDomStrings_js_1.HTMLDomStrings(dom);
    _this.domStrings.adaptor = adaptor;
    _this.styles = [];
    return _this;
  }
  HTMLDocument.prototype.findPosition = function (N, index, delim, nodes) {
    var e_1, _a;
    var adaptor = this.adaptor;
    try {
      for (var _b = __values(nodes[N]), _c = _b.next(); !_c.done; _c = _b.next()) {
        var list = _c.value;
        var _d = __read(list, 2),
          node = _d[0],
          n = _d[1];
        if (index <= n && adaptor.kind(node) === '#text') {
          return {
            node: node,
            n: Math.max(index, 0),
            delim: delim
          };
        }
        index -= n;
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
    return {
      node: null,
      n: 0,
      delim: delim
    };
  };
  HTMLDocument.prototype.mathItem = function (item, jax, nodes) {
    var math = item.math;
    var start = this.findPosition(item.n, item.start.n, item.open, nodes);
    var end = this.findPosition(item.n, item.end.n, item.close, nodes);
    return new this.options.MathItem(math, jax, item.display, start, end);
  };
  HTMLDocument.prototype.findMath = function (options) {
    var e_2, _a, e_3, _b, _c, e_4, _d, e_5, _e;
    if (!this.processed.isSet('findMath')) {
      this.adaptor.document = this.document;
      options = (0, Options_js_1.userOptions)({
        elements: this.options.elements || [this.adaptor.body(this.document)]
      }, options);
      try {
        for (var _f = __values(this.adaptor.getElements(options['elements'], this.document)), _g = _f.next(); !_g.done; _g = _f.next()) {
          var container = _g.value;
          var _h = __read([null, null], 2),
            strings = _h[0],
            nodes = _h[1];
          try {
            for (var _j = (e_3 = void 0, __values(this.inputJax)), _k = _j.next(); !_k.done; _k = _j.next()) {
              var jax = _k.value;
              var list = new this.options['MathList']();
              if (jax.processStrings) {
                if (strings === null) {
                  _c = __read(this.domStrings.find(container), 2), strings = _c[0], nodes = _c[1];
                }
                try {
                  for (var _l = (e_4 = void 0, __values(jax.findMath(strings))), _m = _l.next(); !_m.done; _m = _l.next()) {
                    var math = _m.value;
                    list.push(this.mathItem(math, jax, nodes));
                  }
                } catch (e_4_1) {
                  e_4 = {
                    error: e_4_1
                  };
                } finally {
                  try {
                    if (_m && !_m.done && (_d = _l.return)) _d.call(_l);
                  } finally {
                    if (e_4) throw e_4.error;
                  }
                }
              } else {
                try {
                  for (var _o = (e_5 = void 0, __values(jax.findMath(container))), _p = _o.next(); !_p.done; _p = _o.next()) {
                    var math = _p.value;
                    var item = new this.options.MathItem(math.math, jax, math.display, math.start, math.end);
                    list.push(item);
                  }
                } catch (e_5_1) {
                  e_5 = {
                    error: e_5_1
                  };
                } finally {
                  try {
                    if (_p && !_p.done && (_e = _o.return)) _e.call(_o);
                  } finally {
                    if (e_5) throw e_5.error;
                  }
                }
              }
              this.math.merge(list);
            }
          } catch (e_3_1) {
            e_3 = {
              error: e_3_1
            };
          } finally {
            try {
              if (_k && !_k.done && (_b = _j.return)) _b.call(_j);
            } finally {
              if (e_3) throw e_3.error;
            }
          }
        }
      } catch (e_2_1) {
        e_2 = {
          error: e_2_1
        };
      } finally {
        try {
          if (_g && !_g.done && (_a = _f.return)) _a.call(_f);
        } finally {
          if (e_2) throw e_2.error;
        }
      }
      this.processed.set('findMath');
    }
    return this;
  };
  HTMLDocument.prototype.updateDocument = function () {
    if (!this.processed.isSet('updateDocument')) {
      this.addPageElements();
      this.addStyleSheet();
      _super.prototype.updateDocument.call(this);
      this.processed.set('updateDocument');
    }
    return this;
  };
  HTMLDocument.prototype.addPageElements = function () {
    var body = this.adaptor.body(this.document);
    var node = this.documentPageElements();
    if (node) {
      this.adaptor.append(body, node);
    }
  };
  HTMLDocument.prototype.addStyleSheet = function () {
    var sheet = this.documentStyleSheet();
    var adaptor = this.adaptor;
    if (sheet && !adaptor.parent(sheet)) {
      var head = adaptor.head(this.document);
      var styles = this.findSheet(head, adaptor.getAttribute(sheet, 'id'));
      if (styles) {
        adaptor.replace(sheet, styles);
      } else {
        adaptor.append(head, sheet);
      }
    }
  };
  HTMLDocument.prototype.findSheet = function (head, id) {
    var e_6, _a;
    if (id) {
      try {
        for (var _b = __values(this.adaptor.tags(head, 'style')), _c = _b.next(); !_c.done; _c = _b.next()) {
          var sheet = _c.value;
          if (this.adaptor.getAttribute(sheet, 'id') === id) {
            return sheet;
          }
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
    return null;
  };
  HTMLDocument.prototype.removeFromDocument = function (restore) {
    var e_7, _a;
    if (restore === void 0) {
      restore = false;
    }
    if (this.processed.isSet('updateDocument')) {
      try {
        for (var _b = __values(this.math), _c = _b.next(); !_c.done; _c = _b.next()) {
          var math = _c.value;
          if (math.state() >= MathItem_js_1.STATE.INSERTED) {
            math.state(MathItem_js_1.STATE.TYPESET, restore);
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
    }
    this.processed.clear('updateDocument');
    return this;
  };
  HTMLDocument.prototype.documentStyleSheet = function () {
    return this.outputJax.styleSheet(this);
  };
  HTMLDocument.prototype.documentPageElements = function () {
    return this.outputJax.pageElements(this);
  };
  HTMLDocument.prototype.addStyles = function (styles) {
    this.styles.push(styles);
  };
  HTMLDocument.prototype.getStyles = function () {
    return this.styles;
  };
  HTMLDocument.KIND = 'HTML';
  HTMLDocument.OPTIONS = __assign(__assign({}, MathDocument_js_1.AbstractMathDocument.OPTIONS), {
    renderActions: (0, Options_js_1.expandable)(__assign(__assign({}, MathDocument_js_1.AbstractMathDocument.OPTIONS.renderActions), {
      styles: [MathItem_js_1.STATE.INSERTED + 1, '', 'updateStyleSheet', false]
    })),
    MathList: HTMLMathList_js_1.HTMLMathList,
    MathItem: HTMLMathItem_js_1.HTMLMathItem,
    DomStrings: null
  });
  return HTMLDocument;
}(MathDocument_js_1.AbstractMathDocument);
exports.HTMLDocument = HTMLDocument;

/***/ }),

/***/ 84915:
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {



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
exports.HTMLDomStrings = void 0;
var Options_js_1 = __webpack_require__(62704);
var HTMLDomStrings = function () {
  function HTMLDomStrings(options) {
    if (options === void 0) {
      options = null;
    }
    var CLASS = this.constructor;
    this.options = (0, Options_js_1.userOptions)((0, Options_js_1.defaultOptions)({}, CLASS.OPTIONS), options);
    this.init();
    this.getPatterns();
  }
  HTMLDomStrings.prototype.init = function () {
    this.strings = [];
    this.string = '';
    this.snodes = [];
    this.nodes = [];
    this.stack = [];
  };
  HTMLDomStrings.prototype.getPatterns = function () {
    var skip = (0, Options_js_1.makeArray)(this.options['skipHtmlTags']);
    var ignore = (0, Options_js_1.makeArray)(this.options['ignoreHtmlClass']);
    var process = (0, Options_js_1.makeArray)(this.options['processHtmlClass']);
    this.skipHtmlTags = new RegExp('^(?:' + skip.join('|') + ')$', 'i');
    this.ignoreHtmlClass = new RegExp('(?:^| )(?:' + ignore.join('|') + ')(?: |$)');
    this.processHtmlClass = new RegExp('(?:^| )(?:' + process + ')(?: |$)');
  };
  HTMLDomStrings.prototype.pushString = function () {
    if (this.string.match(/\S/)) {
      this.strings.push(this.string);
      this.nodes.push(this.snodes);
    }
    this.string = '';
    this.snodes = [];
  };
  HTMLDomStrings.prototype.extendString = function (node, text) {
    this.snodes.push([node, text.length]);
    this.string += text;
  };
  HTMLDomStrings.prototype.handleText = function (node, ignore) {
    if (!ignore) {
      this.extendString(node, this.adaptor.value(node));
    }
    return this.adaptor.next(node);
  };
  HTMLDomStrings.prototype.handleTag = function (node, ignore) {
    if (!ignore) {
      var text = this.options['includeHtmlTags'][this.adaptor.kind(node)];
      this.extendString(node, text);
    }
    return this.adaptor.next(node);
  };
  HTMLDomStrings.prototype.handleContainer = function (node, ignore) {
    this.pushString();
    var cname = this.adaptor.getAttribute(node, 'class') || '';
    var tname = this.adaptor.kind(node) || '';
    var process = this.processHtmlClass.exec(cname);
    var next = node;
    if (this.adaptor.firstChild(node) && !this.adaptor.getAttribute(node, 'data-MJX') && (process || !this.skipHtmlTags.exec(tname))) {
      if (this.adaptor.next(node)) {
        this.stack.push([this.adaptor.next(node), ignore]);
      }
      next = this.adaptor.firstChild(node);
      ignore = (ignore || this.ignoreHtmlClass.exec(cname)) && !process;
    } else {
      next = this.adaptor.next(node);
    }
    return [next, ignore];
  };
  HTMLDomStrings.prototype.handleOther = function (node, _ignore) {
    this.pushString();
    return this.adaptor.next(node);
  };
  HTMLDomStrings.prototype.find = function (node) {
    var _a, _b;
    this.init();
    var stop = this.adaptor.next(node);
    var ignore = false;
    var include = this.options['includeHtmlTags'];
    while (node && node !== stop) {
      var kind = this.adaptor.kind(node);
      if (kind === '#text') {
        node = this.handleText(node, ignore);
      } else if (include.hasOwnProperty(kind)) {
        node = this.handleTag(node, ignore);
      } else if (kind) {
        _a = __read(this.handleContainer(node, ignore), 2), node = _a[0], ignore = _a[1];
      } else {
        node = this.handleOther(node, ignore);
      }
      if (!node && this.stack.length) {
        this.pushString();
        _b = __read(this.stack.pop(), 2), node = _b[0], ignore = _b[1];
      }
    }
    this.pushString();
    var result = [this.strings, this.nodes];
    this.init();
    return result;
  };
  HTMLDomStrings.OPTIONS = {
    skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code', 'annotation', 'annotation-xml'],
    includeHtmlTags: {
      br: '\n',
      wbr: '',
      '#comment': ''
    },
    ignoreHtmlClass: 'mathjax_ignore',
    processHtmlClass: 'mathjax_process'
  };
  return HTMLDomStrings;
}();
exports.HTMLDomStrings = HTMLDomStrings;

/***/ }),

/***/ 62464:
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
Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports.HTMLHandler = void 0;
var Handler_js_1 = __webpack_require__(9312);
var HTMLDocument_js_1 = __webpack_require__(98435);
var HTMLHandler = function (_super) {
  __extends(HTMLHandler, _super);
  function HTMLHandler() {
    var _this = _super !== null && _super.apply(this, arguments) || this;
    _this.documentClass = HTMLDocument_js_1.HTMLDocument;
    return _this;
  }
  HTMLHandler.prototype.handlesDocument = function (document) {
    var adaptor = this.adaptor;
    if (typeof document === 'string') {
      try {
        document = adaptor.parse(document, 'text/html');
      } catch (err) {}
    }
    if (document instanceof adaptor.window.Document || document instanceof adaptor.window.HTMLElement || document instanceof adaptor.window.DocumentFragment) {
      return true;
    }
    return false;
  };
  HTMLHandler.prototype.create = function (document, options) {
    var adaptor = this.adaptor;
    if (typeof document === 'string') {
      document = adaptor.parse(document, 'text/html');
    } else if (document instanceof adaptor.window.HTMLElement || document instanceof adaptor.window.DocumentFragment) {
      var child = document;
      document = adaptor.parse('', 'text/html');
      adaptor.append(adaptor.body(document), child);
    }
    return _super.prototype.create.call(this, document, options);
  };
  return HTMLHandler;
}(Handler_js_1.AbstractHandler);
exports.HTMLHandler = HTMLHandler;

/***/ }),

/***/ 92223:
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
Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports.HTMLMathItem = void 0;
var MathItem_js_1 = __webpack_require__(57714);
var HTMLMathItem = function (_super) {
  __extends(HTMLMathItem, _super);
  function HTMLMathItem(math, jax, display, start, end) {
    if (display === void 0) {
      display = true;
    }
    if (start === void 0) {
      start = {
        node: null,
        n: 0,
        delim: ''
      };
    }
    if (end === void 0) {
      end = {
        node: null,
        n: 0,
        delim: ''
      };
    }
    return _super.call(this, math, jax, display, start, end) || this;
  }
  Object.defineProperty(HTMLMathItem.prototype, "adaptor", {
    get: function () {
      return this.inputJax.adaptor;
    },
    enumerable: false,
    configurable: true
  });
  HTMLMathItem.prototype.updateDocument = function (_html) {
    if (this.state() < MathItem_js_1.STATE.INSERTED) {
      if (this.inputJax.processStrings) {
        var node = this.start.node;
        if (node === this.end.node) {
          if (this.end.n && this.end.n < this.adaptor.value(this.end.node).length) {
            this.adaptor.split(this.end.node, this.end.n);
          }
          if (this.start.n) {
            node = this.adaptor.split(this.start.node, this.start.n);
          }
          this.adaptor.replace(this.typesetRoot, node);
        } else {
          if (this.start.n) {
            node = this.adaptor.split(node, this.start.n);
          }
          while (node !== this.end.node) {
            var next = this.adaptor.next(node);
            this.adaptor.remove(node);
            node = next;
          }
          this.adaptor.insert(this.typesetRoot, node);
          if (this.end.n < this.adaptor.value(node).length) {
            this.adaptor.split(node, this.end.n);
          }
          this.adaptor.remove(node);
        }
      } else {
        this.adaptor.replace(this.typesetRoot, this.start.node);
      }
      this.start.node = this.end.node = this.typesetRoot;
      this.start.n = this.end.n = 0;
      this.state(MathItem_js_1.STATE.INSERTED);
    }
  };
  HTMLMathItem.prototype.updateStyleSheet = function (document) {
    document.addStyleSheet();
  };
  HTMLMathItem.prototype.removeFromDocument = function (restore) {
    if (restore === void 0) {
      restore = false;
    }
    if (this.state() >= MathItem_js_1.STATE.TYPESET) {
      var adaptor = this.adaptor;
      var node = this.start.node;
      var math = adaptor.text('');
      if (restore) {
        var text = this.start.delim + this.math + this.end.delim;
        if (this.inputJax.processStrings) {
          math = adaptor.text(text);
        } else {
          var doc = adaptor.parse(text, 'text/html');
          math = adaptor.firstChild(adaptor.body(doc));
        }
      }
      if (adaptor.parent(node)) {
        adaptor.replace(math, node);
      }
      this.start.node = this.end.node = math;
      this.start.n = this.end.n = 0;
    }
  };
  return HTMLMathItem;
}(MathItem_js_1.AbstractMathItem);
exports.HTMLMathItem = HTMLMathItem;

/***/ }),

/***/ 99432:
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
Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports.HTMLMathList = void 0;
var MathList_js_1 = __webpack_require__(82433);
var HTMLMathList = function (_super) {
  __extends(HTMLMathList, _super);
  function HTMLMathList() {
    return _super !== null && _super.apply(this, arguments) || this;
  }
  return HTMLMathList;
}(MathList_js_1.AbstractMathList);
exports.HTMLMathList = HTMLMathList;

/***/ }),

/***/ 37367:
/***/ (function(__unused_webpack_module, exports) {



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
exports.BitFieldClass = exports.BitField = void 0;
var BitField = function () {
  function BitField() {
    this.bits = 0;
  }
  BitField.allocate = function () {
    var e_1, _a;
    var names = [];
    for (var _i = 0; _i < arguments.length; _i++) {
      names[_i] = arguments[_i];
    }
    try {
      for (var names_1 = __values(names), names_1_1 = names_1.next(); !names_1_1.done; names_1_1 = names_1.next()) {
        var name_1 = names_1_1.value;
        if (this.has(name_1)) {
          throw new Error('Bit already allocated for ' + name_1);
        }
        if (this.next === BitField.MAXBIT) {
          throw new Error('Maximum number of bits already allocated');
        }
        this.names.set(name_1, this.next);
        this.next <<= 1;
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
  };
  BitField.has = function (name) {
    return this.names.has(name);
  };
  BitField.prototype.set = function (name) {
    this.bits |= this.getBit(name);
  };
  BitField.prototype.clear = function (name) {
    this.bits &= ~this.getBit(name);
  };
  BitField.prototype.isSet = function (name) {
    return !!(this.bits & this.getBit(name));
  };
  BitField.prototype.reset = function () {
    this.bits = 0;
  };
  BitField.prototype.getBit = function (name) {
    var bit = this.constructor.names.get(name);
    if (!bit) {
      throw new Error('Unknown bit-field name: ' + name);
    }
    return bit;
  };
  BitField.MAXBIT = 1 << 31;
  BitField.next = 1;
  BitField.names = new Map();
  return BitField;
}();
exports.BitField = BitField;
function BitFieldClass() {
  var names = [];
  for (var _i = 0; _i < arguments.length; _i++) {
    names[_i] = arguments[_i];
  }
  var Bits = function (_super) {
    __extends(Bits, _super);
    function Bits() {
      return _super !== null && _super.apply(this, arguments) || this;
    }
    return Bits;
  }(BitField);
  Bits.allocate.apply(Bits, __spreadArray([], __read(names), false));
  return Bits;
}
exports.BitFieldClass = BitFieldClass;

/***/ }),

/***/ 58235:
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
exports.FunctionList = void 0;
var PrioritizedList_js_1 = __webpack_require__(47144);
var FunctionList = function (_super) {
  __extends(FunctionList, _super);
  function FunctionList() {
    return _super !== null && _super.apply(this, arguments) || this;
  }
  FunctionList.prototype.execute = function () {
    var e_1, _a;
    var data = [];
    for (var _i = 0; _i < arguments.length; _i++) {
      data[_i] = arguments[_i];
    }
    try {
      for (var _b = __values(this), _c = _b.next(); !_c.done; _c = _b.next()) {
        var item = _c.value;
        var result = item.item.apply(item, __spreadArray([], __read(data), false));
        if (result === false) {
          return false;
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
    return true;
  };
  FunctionList.prototype.asyncExecute = function () {
    var data = [];
    for (var _i = 0; _i < arguments.length; _i++) {
      data[_i] = arguments[_i];
    }
    var i = -1;
    var items = this.items;
    return new Promise(function (ok, fail) {
      (function execute() {
        var _a;
        while (++i < items.length) {
          var result = (_a = items[i]).item.apply(_a, __spreadArray([], __read(data), false));
          if (result instanceof Promise) {
            result.then(execute).catch(function (err) {
              return fail(err);
            });
            return;
          }
          if (result === false) {
            ok(false);
            return;
          }
        }
        ok(true);
      })();
    });
  };
  return FunctionList;
}(PrioritizedList_js_1.PrioritizedList);
exports.FunctionList = FunctionList;

/***/ }),

/***/ 4717:
/***/ (function(__unused_webpack_module, exports) {



var __generator = this && this.__generator || function (thisArg, body) {
  var _ = {
      label: 0,
      sent: function () {
        if (t[0] & 1) throw t[1];
        return t[1];
      },
      trys: [],
      ops: []
    },
    f,
    y,
    t,
    g;
  return g = {
    next: verb(0),
    "throw": verb(1),
    "return": verb(2)
  }, typeof Symbol === "function" && (g[Symbol.iterator] = function () {
    return this;
  }), g;
  function verb(n) {
    return function (v) {
      return step([n, v]);
    };
  }
  function step(op) {
    if (f) throw new TypeError("Generator is already executing.");
    while (_) try {
      if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
      if (y = 0, t) op = [op[0] & 2, t.value];
      switch (op[0]) {
        case 0:
        case 1:
          t = op;
          break;
        case 4:
          _.label++;
          return {
            value: op[1],
            done: false
          };
        case 5:
          _.label++;
          y = op[1];
          op = [0];
          continue;
        case 7:
          op = _.ops.pop();
          _.trys.pop();
          continue;
        default:
          if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) {
            _ = 0;
            continue;
          }
          if (op[0] === 3 && (!t || op[1] > t[0] && op[1] < t[3])) {
            _.label = op[1];
            break;
          }
          if (op[0] === 6 && _.label < t[1]) {
            _.label = t[1];
            t = op;
            break;
          }
          if (t && _.label < t[2]) {
            _.label = t[2];
            _.ops.push(op);
            break;
          }
          if (t[2]) _.ops.pop();
          _.trys.pop();
          continue;
      }
      op = body.call(thisArg, _);
    } catch (e) {
      op = [6, e];
      y = 0;
    } finally {
      f = t = 0;
    }
    if (op[0] & 5) throw op[1];
    return {
      value: op[0] ? op[1] : void 0,
      done: true
    };
  }
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
exports.LinkedList = exports.ListItem = exports.END = void 0;
exports.END = Symbol();
var ListItem = function () {
  function ListItem(data) {
    if (data === void 0) {
      data = null;
    }
    this.next = null;
    this.prev = null;
    this.data = data;
  }
  return ListItem;
}();
exports.ListItem = ListItem;
var LinkedList = function () {
  function LinkedList() {
    var args = [];
    for (var _i = 0; _i < arguments.length; _i++) {
      args[_i] = arguments[_i];
    }
    this.list = new ListItem(exports.END);
    this.list.next = this.list.prev = this.list;
    this.push.apply(this, __spreadArray([], __read(args), false));
  }
  LinkedList.prototype.isBefore = function (a, b) {
    return a < b;
  };
  LinkedList.prototype.push = function () {
    var e_1, _a;
    var args = [];
    for (var _i = 0; _i < arguments.length; _i++) {
      args[_i] = arguments[_i];
    }
    try {
      for (var args_1 = __values(args), args_1_1 = args_1.next(); !args_1_1.done; args_1_1 = args_1.next()) {
        var data = args_1_1.value;
        var item = new ListItem(data);
        item.next = this.list;
        item.prev = this.list.prev;
        this.list.prev = item;
        item.prev.next = item;
      }
    } catch (e_1_1) {
      e_1 = {
        error: e_1_1
      };
    } finally {
      try {
        if (args_1_1 && !args_1_1.done && (_a = args_1.return)) _a.call(args_1);
      } finally {
        if (e_1) throw e_1.error;
      }
    }
    return this;
  };
  LinkedList.prototype.pop = function () {
    var item = this.list.prev;
    if (item.data === exports.END) {
      return null;
    }
    this.list.prev = item.prev;
    item.prev.next = this.list;
    item.next = item.prev = null;
    return item.data;
  };
  LinkedList.prototype.unshift = function () {
    var e_2, _a;
    var args = [];
    for (var _i = 0; _i < arguments.length; _i++) {
      args[_i] = arguments[_i];
    }
    try {
      for (var _b = __values(args.slice(0).reverse()), _c = _b.next(); !_c.done; _c = _b.next()) {
        var data = _c.value;
        var item = new ListItem(data);
        item.next = this.list.next;
        item.prev = this.list;
        this.list.next = item;
        item.next.prev = item;
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
    return this;
  };
  LinkedList.prototype.shift = function () {
    var item = this.list.next;
    if (item.data === exports.END) {
      return null;
    }
    this.list.next = item.next;
    item.next.prev = this.list;
    item.next = item.prev = null;
    return item.data;
  };
  LinkedList.prototype.remove = function () {
    var e_3, _a;
    var items = [];
    for (var _i = 0; _i < arguments.length; _i++) {
      items[_i] = arguments[_i];
    }
    var map = new Map();
    try {
      for (var items_1 = __values(items), items_1_1 = items_1.next(); !items_1_1.done; items_1_1 = items_1.next()) {
        var item_1 = items_1_1.value;
        map.set(item_1, true);
      }
    } catch (e_3_1) {
      e_3 = {
        error: e_3_1
      };
    } finally {
      try {
        if (items_1_1 && !items_1_1.done && (_a = items_1.return)) _a.call(items_1);
      } finally {
        if (e_3) throw e_3.error;
      }
    }
    var item = this.list.next;
    while (item.data !== exports.END) {
      var next = item.next;
      if (map.has(item.data)) {
        item.prev.next = item.next;
        item.next.prev = item.prev;
        item.next = item.prev = null;
      }
      item = next;
    }
  };
  LinkedList.prototype.clear = function () {
    this.list.next.prev = this.list.prev.next = null;
    this.list.next = this.list.prev = this.list;
    return this;
  };
  LinkedList.prototype[Symbol.iterator] = function () {
    var current;
    return __generator(this, function (_a) {
      switch (_a.label) {
        case 0:
          current = this.list.next;
          _a.label = 1;
        case 1:
          if (!(current.data !== exports.END)) return [3, 3];
          return [4, current.data];
        case 2:
          _a.sent();
          current = current.next;
          return [3, 1];
        case 3:
          return [2];
      }
    });
  };
  LinkedList.prototype.reversed = function () {
    var current;
    return __generator(this, function (_a) {
      switch (_a.label) {
        case 0:
          current = this.list.prev;
          _a.label = 1;
        case 1:
          if (!(current.data !== exports.END)) return [3, 3];
          return [4, current.data];
        case 2:
          _a.sent();
          current = current.prev;
          return [3, 1];
        case 3:
          return [2];
      }
    });
  };
  LinkedList.prototype.insert = function (data, isBefore) {
    if (isBefore === void 0) {
      isBefore = null;
    }
    if (isBefore === null) {
      isBefore = this.isBefore.bind(this);
    }
    var item = new ListItem(data);
    var cur = this.list.next;
    while (cur.data !== exports.END && isBefore(cur.data, item.data)) {
      cur = cur.next;
    }
    item.prev = cur.prev;
    item.next = cur;
    cur.prev.next = cur.prev = item;
    return this;
  };
  LinkedList.prototype.sort = function (isBefore) {
    var e_4, _a;
    if (isBefore === void 0) {
      isBefore = null;
    }
    if (isBefore === null) {
      isBefore = this.isBefore.bind(this);
    }
    var lists = [];
    try {
      for (var _b = __values(this), _c = _b.next(); !_c.done; _c = _b.next()) {
        var item = _c.value;
        lists.push(new LinkedList(item));
      }
    } catch (e_4_1) {
      e_4 = {
        error: e_4_1
      };
    } finally {
      try {
        if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
      } finally {
        if (e_4) throw e_4.error;
      }
    }
    this.list.next = this.list.prev = this.list;
    while (lists.length > 1) {
      var l1 = lists.shift();
      var l2 = lists.shift();
      l1.merge(l2, isBefore);
      lists.push(l1);
    }
    if (lists.length) {
      this.list = lists[0].list;
    }
    return this;
  };
  LinkedList.prototype.merge = function (list, isBefore) {
    var _a, _b, _c, _d, _e;
    if (isBefore === void 0) {
      isBefore = null;
    }
    if (isBefore === null) {
      isBefore = this.isBefore.bind(this);
    }
    var lcur = this.list.next;
    var mcur = list.list.next;
    while (lcur.data !== exports.END && mcur.data !== exports.END) {
      if (isBefore(mcur.data, lcur.data)) {
        _a = __read([lcur, mcur], 2), mcur.prev.next = _a[0], lcur.prev.next = _a[1];
        _b = __read([lcur.prev, mcur.prev], 2), mcur.prev = _b[0], lcur.prev = _b[1];
        _c = __read([list.list, this.list], 2), this.list.prev.next = _c[0], list.list.prev.next = _c[1];
        _d = __read([list.list.prev, this.list.prev], 2), this.list.prev = _d[0], list.list.prev = _d[1];
        _e = __read([mcur.next, lcur], 2), lcur = _e[0], mcur = _e[1];
      } else {
        lcur = lcur.next;
      }
    }
    if (mcur.data !== exports.END) {
      this.list.prev.next = list.list.next;
      list.list.next.prev = this.list.prev;
      list.list.prev.next = this.list;
      this.list.prev = list.list.prev;
      list.list.next = list.list.prev = list.list;
    }
    return this;
  };
  return LinkedList;
}();
exports.LinkedList = LinkedList;

/***/ }),

/***/ 47144:
/***/ ((__unused_webpack_module, exports) => {



Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports.PrioritizedList = void 0;
var PrioritizedList = function () {
  function PrioritizedList() {
    this.items = [];
    this.items = [];
  }
  PrioritizedList.prototype[Symbol.iterator] = function () {
    var i = 0;
    var items = this.items;
    return {
      next: function () {
        return {
          value: items[i++],
          done: i > items.length
        };
      }
    };
  };
  PrioritizedList.prototype.add = function (item, priority) {
    if (priority === void 0) {
      priority = PrioritizedList.DEFAULTPRIORITY;
    }
    var i = this.items.length;
    do {
      i--;
    } while (i >= 0 && priority < this.items[i].priority);
    this.items.splice(i + 1, 0, {
      item: item,
      priority: priority
    });
    return item;
  };
  PrioritizedList.prototype.remove = function (item) {
    var i = this.items.length;
    do {
      i--;
    } while (i >= 0 && this.items[i].item !== item);
    if (i >= 0) {
      this.items.splice(i, 1);
    }
  };
  PrioritizedList.DEFAULTPRIORITY = 5;
  return PrioritizedList;
}();
exports.PrioritizedList = PrioritizedList;

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiMjQ2NC5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7QUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7Ozs7Ozs7QUMzREE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7Ozs7Ozs7QUMvREE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOzs7Ozs7O0FDbnNCQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOzs7Ozs7O0FDckNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7Ozs7Ozs7QUN2REE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOzs7Ozs7O0FDblVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7Ozs7Ozs7QUMzSUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7Ozs7Ozs7QUM1REE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7Ozs7Ozs7QUN4SEE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7Ozs7OztBQ2xDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7Ozs7OztBQ3RKQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7Ozs7OztBQ3ZJQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOzs7Ozs7O0FDdFpBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AZGF0YWxheWVyL2p1cHl0ZXItdmlld2VyLy4vbm9kZV9tb2R1bGVzL21hdGhqYXgtZnVsbC9qcy9jb3JlL0hhbmRsZXIuanMiLCJ3ZWJwYWNrOi8vQGRhdGFsYXllci9qdXB5dGVyLXZpZXdlci8uL25vZGVfbW9kdWxlcy9tYXRoamF4LWZ1bGwvanMvY29yZS9JbnB1dEpheC5qcyIsIndlYnBhY2s6Ly9AZGF0YWxheWVyL2p1cHl0ZXItdmlld2VyLy4vbm9kZV9tb2R1bGVzL21hdGhqYXgtZnVsbC9qcy9jb3JlL01hdGhEb2N1bWVudC5qcyIsIndlYnBhY2s6Ly9AZGF0YWxheWVyL2p1cHl0ZXItdmlld2VyLy4vbm9kZV9tb2R1bGVzL21hdGhqYXgtZnVsbC9qcy9jb3JlL01hdGhMaXN0LmpzIiwid2VicGFjazovL0BkYXRhbGF5ZXIvanVweXRlci12aWV3ZXIvLi9ub2RlX21vZHVsZXMvbWF0aGpheC1mdWxsL2pzL2NvcmUvT3V0cHV0SmF4LmpzIiwid2VicGFjazovL0BkYXRhbGF5ZXIvanVweXRlci12aWV3ZXIvLi9ub2RlX21vZHVsZXMvbWF0aGpheC1mdWxsL2pzL2hhbmRsZXJzL2h0bWwvSFRNTERvY3VtZW50LmpzIiwid2VicGFjazovL0BkYXRhbGF5ZXIvanVweXRlci12aWV3ZXIvLi9ub2RlX21vZHVsZXMvbWF0aGpheC1mdWxsL2pzL2hhbmRsZXJzL2h0bWwvSFRNTERvbVN0cmluZ3MuanMiLCJ3ZWJwYWNrOi8vQGRhdGFsYXllci9qdXB5dGVyLXZpZXdlci8uL25vZGVfbW9kdWxlcy9tYXRoamF4LWZ1bGwvanMvaGFuZGxlcnMvaHRtbC9IVE1MSGFuZGxlci5qcyIsIndlYnBhY2s6Ly9AZGF0YWxheWVyL2p1cHl0ZXItdmlld2VyLy4vbm9kZV9tb2R1bGVzL21hdGhqYXgtZnVsbC9qcy9oYW5kbGVycy9odG1sL0hUTUxNYXRoSXRlbS5qcyIsIndlYnBhY2s6Ly9AZGF0YWxheWVyL2p1cHl0ZXItdmlld2VyLy4vbm9kZV9tb2R1bGVzL21hdGhqYXgtZnVsbC9qcy9oYW5kbGVycy9odG1sL0hUTUxNYXRoTGlzdC5qcyIsIndlYnBhY2s6Ly9AZGF0YWxheWVyL2p1cHl0ZXItdmlld2VyLy4vbm9kZV9tb2R1bGVzL21hdGhqYXgtZnVsbC9qcy91dGlsL0JpdEZpZWxkLmpzIiwid2VicGFjazovL0BkYXRhbGF5ZXIvanVweXRlci12aWV3ZXIvLi9ub2RlX21vZHVsZXMvbWF0aGpheC1mdWxsL2pzL3V0aWwvRnVuY3Rpb25MaXN0LmpzIiwid2VicGFjazovL0BkYXRhbGF5ZXIvanVweXRlci12aWV3ZXIvLi9ub2RlX21vZHVsZXMvbWF0aGpheC1mdWxsL2pzL3V0aWwvTGlua2VkTGlzdC5qcyIsIndlYnBhY2s6Ly9AZGF0YWxheWVyL2p1cHl0ZXItdmlld2VyLy4vbm9kZV9tb2R1bGVzL21hdGhqYXgtZnVsbC9qcy91dGlsL1ByaW9yaXRpemVkTGlzdC5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyJcInVzZSBzdHJpY3RcIjtcblxudmFyIF9fZXh0ZW5kcyA9IHRoaXMgJiYgdGhpcy5fX2V4dGVuZHMgfHwgZnVuY3Rpb24gKCkge1xuICB2YXIgZXh0ZW5kU3RhdGljcyA9IGZ1bmN0aW9uIChkLCBiKSB7XG4gICAgZXh0ZW5kU3RhdGljcyA9IE9iamVjdC5zZXRQcm90b3R5cGVPZiB8fCB7XG4gICAgICBfX3Byb3RvX186IFtdXG4gICAgfSBpbnN0YW5jZW9mIEFycmF5ICYmIGZ1bmN0aW9uIChkLCBiKSB7XG4gICAgICBkLl9fcHJvdG9fXyA9IGI7XG4gICAgfSB8fCBmdW5jdGlvbiAoZCwgYikge1xuICAgICAgZm9yICh2YXIgcCBpbiBiKSBpZiAoT2JqZWN0LnByb3RvdHlwZS5oYXNPd25Qcm9wZXJ0eS5jYWxsKGIsIHApKSBkW3BdID0gYltwXTtcbiAgICB9O1xuICAgIHJldHVybiBleHRlbmRTdGF0aWNzKGQsIGIpO1xuICB9O1xuICByZXR1cm4gZnVuY3Rpb24gKGQsIGIpIHtcbiAgICBpZiAodHlwZW9mIGIgIT09IFwiZnVuY3Rpb25cIiAmJiBiICE9PSBudWxsKSB0aHJvdyBuZXcgVHlwZUVycm9yKFwiQ2xhc3MgZXh0ZW5kcyB2YWx1ZSBcIiArIFN0cmluZyhiKSArIFwiIGlzIG5vdCBhIGNvbnN0cnVjdG9yIG9yIG51bGxcIik7XG4gICAgZXh0ZW5kU3RhdGljcyhkLCBiKTtcbiAgICBmdW5jdGlvbiBfXygpIHtcbiAgICAgIHRoaXMuY29uc3RydWN0b3IgPSBkO1xuICAgIH1cbiAgICBkLnByb3RvdHlwZSA9IGIgPT09IG51bGwgPyBPYmplY3QuY3JlYXRlKGIpIDogKF9fLnByb3RvdHlwZSA9IGIucHJvdG90eXBlLCBuZXcgX18oKSk7XG4gIH07XG59KCk7XG5PYmplY3QuZGVmaW5lUHJvcGVydHkoZXhwb3J0cywgXCJfX2VzTW9kdWxlXCIsIHtcbiAgdmFsdWU6IHRydWVcbn0pO1xuZXhwb3J0cy5BYnN0cmFjdEhhbmRsZXIgPSB2b2lkIDA7XG52YXIgTWF0aERvY3VtZW50X2pzXzEgPSByZXF1aXJlKFwiLi9NYXRoRG9jdW1lbnQuanNcIik7XG52YXIgRGVmYXVsdE1hdGhEb2N1bWVudCA9IGZ1bmN0aW9uIChfc3VwZXIpIHtcbiAgX19leHRlbmRzKERlZmF1bHRNYXRoRG9jdW1lbnQsIF9zdXBlcik7XG4gIGZ1bmN0aW9uIERlZmF1bHRNYXRoRG9jdW1lbnQoKSB7XG4gICAgcmV0dXJuIF9zdXBlciAhPT0gbnVsbCAmJiBfc3VwZXIuYXBwbHkodGhpcywgYXJndW1lbnRzKSB8fCB0aGlzO1xuICB9XG4gIHJldHVybiBEZWZhdWx0TWF0aERvY3VtZW50O1xufShNYXRoRG9jdW1lbnRfanNfMS5BYnN0cmFjdE1hdGhEb2N1bWVudCk7XG52YXIgQWJzdHJhY3RIYW5kbGVyID0gZnVuY3Rpb24gKCkge1xuICBmdW5jdGlvbiBBYnN0cmFjdEhhbmRsZXIoYWRhcHRvciwgcHJpb3JpdHkpIHtcbiAgICBpZiAocHJpb3JpdHkgPT09IHZvaWQgMCkge1xuICAgICAgcHJpb3JpdHkgPSA1O1xuICAgIH1cbiAgICB0aGlzLmRvY3VtZW50Q2xhc3MgPSBEZWZhdWx0TWF0aERvY3VtZW50O1xuICAgIHRoaXMuYWRhcHRvciA9IGFkYXB0b3I7XG4gICAgdGhpcy5wcmlvcml0eSA9IHByaW9yaXR5O1xuICB9XG4gIE9iamVjdC5kZWZpbmVQcm9wZXJ0eShBYnN0cmFjdEhhbmRsZXIucHJvdG90eXBlLCBcIm5hbWVcIiwge1xuICAgIGdldDogZnVuY3Rpb24gKCkge1xuICAgICAgcmV0dXJuIHRoaXMuY29uc3RydWN0b3IuTkFNRTtcbiAgICB9LFxuICAgIGVudW1lcmFibGU6IGZhbHNlLFxuICAgIGNvbmZpZ3VyYWJsZTogdHJ1ZVxuICB9KTtcbiAgQWJzdHJhY3RIYW5kbGVyLnByb3RvdHlwZS5oYW5kbGVzRG9jdW1lbnQgPSBmdW5jdGlvbiAoX2RvY3VtZW50KSB7XG4gICAgcmV0dXJuIGZhbHNlO1xuICB9O1xuICBBYnN0cmFjdEhhbmRsZXIucHJvdG90eXBlLmNyZWF0ZSA9IGZ1bmN0aW9uIChkb2N1bWVudCwgb3B0aW9ucykge1xuICAgIHJldHVybiBuZXcgdGhpcy5kb2N1bWVudENsYXNzKGRvY3VtZW50LCB0aGlzLmFkYXB0b3IsIG9wdGlvbnMpO1xuICB9O1xuICBBYnN0cmFjdEhhbmRsZXIuTkFNRSA9ICdnZW5lcmljJztcbiAgcmV0dXJuIEFic3RyYWN0SGFuZGxlcjtcbn0oKTtcbmV4cG9ydHMuQWJzdHJhY3RIYW5kbGVyID0gQWJzdHJhY3RIYW5kbGVyOyIsIlwidXNlIHN0cmljdFwiO1xuXG5PYmplY3QuZGVmaW5lUHJvcGVydHkoZXhwb3J0cywgXCJfX2VzTW9kdWxlXCIsIHtcbiAgdmFsdWU6IHRydWVcbn0pO1xuZXhwb3J0cy5BYnN0cmFjdElucHV0SmF4ID0gdm9pZCAwO1xudmFyIE9wdGlvbnNfanNfMSA9IHJlcXVpcmUoXCIuLi91dGlsL09wdGlvbnMuanNcIik7XG52YXIgRnVuY3Rpb25MaXN0X2pzXzEgPSByZXF1aXJlKFwiLi4vdXRpbC9GdW5jdGlvbkxpc3QuanNcIik7XG52YXIgQWJzdHJhY3RJbnB1dEpheCA9IGZ1bmN0aW9uICgpIHtcbiAgZnVuY3Rpb24gQWJzdHJhY3RJbnB1dEpheChvcHRpb25zKSB7XG4gICAgaWYgKG9wdGlvbnMgPT09IHZvaWQgMCkge1xuICAgICAgb3B0aW9ucyA9IHt9O1xuICAgIH1cbiAgICB0aGlzLmFkYXB0b3IgPSBudWxsO1xuICAgIHRoaXMubW1sRmFjdG9yeSA9IG51bGw7XG4gICAgdmFyIENMQVNTID0gdGhpcy5jb25zdHJ1Y3RvcjtcbiAgICB0aGlzLm9wdGlvbnMgPSAoMCwgT3B0aW9uc19qc18xLnVzZXJPcHRpb25zKSgoMCwgT3B0aW9uc19qc18xLmRlZmF1bHRPcHRpb25zKSh7fSwgQ0xBU1MuT1BUSU9OUyksIG9wdGlvbnMpO1xuICAgIHRoaXMucHJlRmlsdGVycyA9IG5ldyBGdW5jdGlvbkxpc3RfanNfMS5GdW5jdGlvbkxpc3QoKTtcbiAgICB0aGlzLnBvc3RGaWx0ZXJzID0gbmV3IEZ1bmN0aW9uTGlzdF9qc18xLkZ1bmN0aW9uTGlzdCgpO1xuICB9XG4gIE9iamVjdC5kZWZpbmVQcm9wZXJ0eShBYnN0cmFjdElucHV0SmF4LnByb3RvdHlwZSwgXCJuYW1lXCIsIHtcbiAgICBnZXQ6IGZ1bmN0aW9uICgpIHtcbiAgICAgIHJldHVybiB0aGlzLmNvbnN0cnVjdG9yLk5BTUU7XG4gICAgfSxcbiAgICBlbnVtZXJhYmxlOiBmYWxzZSxcbiAgICBjb25maWd1cmFibGU6IHRydWVcbiAgfSk7XG4gIEFic3RyYWN0SW5wdXRKYXgucHJvdG90eXBlLnNldEFkYXB0b3IgPSBmdW5jdGlvbiAoYWRhcHRvcikge1xuICAgIHRoaXMuYWRhcHRvciA9IGFkYXB0b3I7XG4gIH07XG4gIEFic3RyYWN0SW5wdXRKYXgucHJvdG90eXBlLnNldE1tbEZhY3RvcnkgPSBmdW5jdGlvbiAobW1sRmFjdG9yeSkge1xuICAgIHRoaXMubW1sRmFjdG9yeSA9IG1tbEZhY3Rvcnk7XG4gIH07XG4gIEFic3RyYWN0SW5wdXRKYXgucHJvdG90eXBlLmluaXRpYWxpemUgPSBmdW5jdGlvbiAoKSB7fTtcbiAgQWJzdHJhY3RJbnB1dEpheC5wcm90b3R5cGUucmVzZXQgPSBmdW5jdGlvbiAoKSB7XG4gICAgdmFyIF9hcmdzID0gW107XG4gICAgZm9yICh2YXIgX2kgPSAwOyBfaSA8IGFyZ3VtZW50cy5sZW5ndGg7IF9pKyspIHtcbiAgICAgIF9hcmdzW19pXSA9IGFyZ3VtZW50c1tfaV07XG4gICAgfVxuICB9O1xuICBPYmplY3QuZGVmaW5lUHJvcGVydHkoQWJzdHJhY3RJbnB1dEpheC5wcm90b3R5cGUsIFwicHJvY2Vzc1N0cmluZ3NcIiwge1xuICAgIGdldDogZnVuY3Rpb24gKCkge1xuICAgICAgcmV0dXJuIHRydWU7XG4gICAgfSxcbiAgICBlbnVtZXJhYmxlOiBmYWxzZSxcbiAgICBjb25maWd1cmFibGU6IHRydWVcbiAgfSk7XG4gIEFic3RyYWN0SW5wdXRKYXgucHJvdG90eXBlLmZpbmRNYXRoID0gZnVuY3Rpb24gKF9ub2RlLCBfb3B0aW9ucykge1xuICAgIHJldHVybiBbXTtcbiAgfTtcbiAgQWJzdHJhY3RJbnB1dEpheC5wcm90b3R5cGUuZXhlY3V0ZUZpbHRlcnMgPSBmdW5jdGlvbiAoZmlsdGVycywgbWF0aCwgZG9jdW1lbnQsIGRhdGEpIHtcbiAgICB2YXIgYXJncyA9IHtcbiAgICAgIG1hdGg6IG1hdGgsXG4gICAgICBkb2N1bWVudDogZG9jdW1lbnQsXG4gICAgICBkYXRhOiBkYXRhXG4gICAgfTtcbiAgICBmaWx0ZXJzLmV4ZWN1dGUoYXJncyk7XG4gICAgcmV0dXJuIGFyZ3MuZGF0YTtcbiAgfTtcbiAgQWJzdHJhY3RJbnB1dEpheC5OQU1FID0gJ2dlbmVyaWMnO1xuICBBYnN0cmFjdElucHV0SmF4Lk9QVElPTlMgPSB7fTtcbiAgcmV0dXJuIEFic3RyYWN0SW5wdXRKYXg7XG59KCk7XG5leHBvcnRzLkFic3RyYWN0SW5wdXRKYXggPSBBYnN0cmFjdElucHV0SmF4OyIsIlwidXNlIHN0cmljdFwiO1xuXG52YXIgX19leHRlbmRzID0gdGhpcyAmJiB0aGlzLl9fZXh0ZW5kcyB8fCBmdW5jdGlvbiAoKSB7XG4gIHZhciBleHRlbmRTdGF0aWNzID0gZnVuY3Rpb24gKGQsIGIpIHtcbiAgICBleHRlbmRTdGF0aWNzID0gT2JqZWN0LnNldFByb3RvdHlwZU9mIHx8IHtcbiAgICAgIF9fcHJvdG9fXzogW11cbiAgICB9IGluc3RhbmNlb2YgQXJyYXkgJiYgZnVuY3Rpb24gKGQsIGIpIHtcbiAgICAgIGQuX19wcm90b19fID0gYjtcbiAgICB9IHx8IGZ1bmN0aW9uIChkLCBiKSB7XG4gICAgICBmb3IgKHZhciBwIGluIGIpIGlmIChPYmplY3QucHJvdG90eXBlLmhhc093blByb3BlcnR5LmNhbGwoYiwgcCkpIGRbcF0gPSBiW3BdO1xuICAgIH07XG4gICAgcmV0dXJuIGV4dGVuZFN0YXRpY3MoZCwgYik7XG4gIH07XG4gIHJldHVybiBmdW5jdGlvbiAoZCwgYikge1xuICAgIGlmICh0eXBlb2YgYiAhPT0gXCJmdW5jdGlvblwiICYmIGIgIT09IG51bGwpIHRocm93IG5ldyBUeXBlRXJyb3IoXCJDbGFzcyBleHRlbmRzIHZhbHVlIFwiICsgU3RyaW5nKGIpICsgXCIgaXMgbm90IGEgY29uc3RydWN0b3Igb3IgbnVsbFwiKTtcbiAgICBleHRlbmRTdGF0aWNzKGQsIGIpO1xuICAgIGZ1bmN0aW9uIF9fKCkge1xuICAgICAgdGhpcy5jb25zdHJ1Y3RvciA9IGQ7XG4gICAgfVxuICAgIGQucHJvdG90eXBlID0gYiA9PT0gbnVsbCA/IE9iamVjdC5jcmVhdGUoYikgOiAoX18ucHJvdG90eXBlID0gYi5wcm90b3R5cGUsIG5ldyBfXygpKTtcbiAgfTtcbn0oKTtcbnZhciBfX3ZhbHVlcyA9IHRoaXMgJiYgdGhpcy5fX3ZhbHVlcyB8fCBmdW5jdGlvbiAobykge1xuICB2YXIgcyA9IHR5cGVvZiBTeW1ib2wgPT09IFwiZnVuY3Rpb25cIiAmJiBTeW1ib2wuaXRlcmF0b3IsXG4gICAgbSA9IHMgJiYgb1tzXSxcbiAgICBpID0gMDtcbiAgaWYgKG0pIHJldHVybiBtLmNhbGwobyk7XG4gIGlmIChvICYmIHR5cGVvZiBvLmxlbmd0aCA9PT0gXCJudW1iZXJcIikgcmV0dXJuIHtcbiAgICBuZXh0OiBmdW5jdGlvbiAoKSB7XG4gICAgICBpZiAobyAmJiBpID49IG8ubGVuZ3RoKSBvID0gdm9pZCAwO1xuICAgICAgcmV0dXJuIHtcbiAgICAgICAgdmFsdWU6IG8gJiYgb1tpKytdLFxuICAgICAgICBkb25lOiAhb1xuICAgICAgfTtcbiAgICB9XG4gIH07XG4gIHRocm93IG5ldyBUeXBlRXJyb3IocyA/IFwiT2JqZWN0IGlzIG5vdCBpdGVyYWJsZS5cIiA6IFwiU3ltYm9sLml0ZXJhdG9yIGlzIG5vdCBkZWZpbmVkLlwiKTtcbn07XG52YXIgX19yZWFkID0gdGhpcyAmJiB0aGlzLl9fcmVhZCB8fCBmdW5jdGlvbiAobywgbikge1xuICB2YXIgbSA9IHR5cGVvZiBTeW1ib2wgPT09IFwiZnVuY3Rpb25cIiAmJiBvW1N5bWJvbC5pdGVyYXRvcl07XG4gIGlmICghbSkgcmV0dXJuIG87XG4gIHZhciBpID0gbS5jYWxsKG8pLFxuICAgIHIsXG4gICAgYXIgPSBbXSxcbiAgICBlO1xuICB0cnkge1xuICAgIHdoaWxlICgobiA9PT0gdm9pZCAwIHx8IG4tLSA+IDApICYmICEociA9IGkubmV4dCgpKS5kb25lKSBhci5wdXNoKHIudmFsdWUpO1xuICB9IGNhdGNoIChlcnJvcikge1xuICAgIGUgPSB7XG4gICAgICBlcnJvcjogZXJyb3JcbiAgICB9O1xuICB9IGZpbmFsbHkge1xuICAgIHRyeSB7XG4gICAgICBpZiAociAmJiAhci5kb25lICYmIChtID0gaVtcInJldHVyblwiXSkpIG0uY2FsbChpKTtcbiAgICB9IGZpbmFsbHkge1xuICAgICAgaWYgKGUpIHRocm93IGUuZXJyb3I7XG4gICAgfVxuICB9XG4gIHJldHVybiBhcjtcbn07XG52YXIgX19zcHJlYWRBcnJheSA9IHRoaXMgJiYgdGhpcy5fX3NwcmVhZEFycmF5IHx8IGZ1bmN0aW9uICh0bywgZnJvbSwgcGFjaykge1xuICBpZiAocGFjayB8fCBhcmd1bWVudHMubGVuZ3RoID09PSAyKSBmb3IgKHZhciBpID0gMCwgbCA9IGZyb20ubGVuZ3RoLCBhcjsgaSA8IGw7IGkrKykge1xuICAgIGlmIChhciB8fCAhKGkgaW4gZnJvbSkpIHtcbiAgICAgIGlmICghYXIpIGFyID0gQXJyYXkucHJvdG90eXBlLnNsaWNlLmNhbGwoZnJvbSwgMCwgaSk7XG4gICAgICBhcltpXSA9IGZyb21baV07XG4gICAgfVxuICB9XG4gIHJldHVybiB0by5jb25jYXQoYXIgfHwgQXJyYXkucHJvdG90eXBlLnNsaWNlLmNhbGwoZnJvbSkpO1xufTtcbk9iamVjdC5kZWZpbmVQcm9wZXJ0eShleHBvcnRzLCBcIl9fZXNNb2R1bGVcIiwge1xuICB2YWx1ZTogdHJ1ZVxufSk7XG5leHBvcnRzLkFic3RyYWN0TWF0aERvY3VtZW50ID0gZXhwb3J0cy5yZXNldEFsbE9wdGlvbnMgPSBleHBvcnRzLnJlc2V0T3B0aW9ucyA9IGV4cG9ydHMuUmVuZGVyTGlzdCA9IHZvaWQgMDtcbnZhciBPcHRpb25zX2pzXzEgPSByZXF1aXJlKFwiLi4vdXRpbC9PcHRpb25zLmpzXCIpO1xudmFyIElucHV0SmF4X2pzXzEgPSByZXF1aXJlKFwiLi9JbnB1dEpheC5qc1wiKTtcbnZhciBPdXRwdXRKYXhfanNfMSA9IHJlcXVpcmUoXCIuL091dHB1dEpheC5qc1wiKTtcbnZhciBNYXRoTGlzdF9qc18xID0gcmVxdWlyZShcIi4vTWF0aExpc3QuanNcIik7XG52YXIgTWF0aEl0ZW1fanNfMSA9IHJlcXVpcmUoXCIuL01hdGhJdGVtLmpzXCIpO1xudmFyIE1tbEZhY3RvcnlfanNfMSA9IHJlcXVpcmUoXCIuLi9jb3JlL01tbFRyZWUvTW1sRmFjdG9yeS5qc1wiKTtcbnZhciBCaXRGaWVsZF9qc18xID0gcmVxdWlyZShcIi4uL3V0aWwvQml0RmllbGQuanNcIik7XG52YXIgUHJpb3JpdGl6ZWRMaXN0X2pzXzEgPSByZXF1aXJlKFwiLi4vdXRpbC9Qcmlvcml0aXplZExpc3QuanNcIik7XG52YXIgUmVuZGVyTGlzdCA9IGZ1bmN0aW9uIChfc3VwZXIpIHtcbiAgX19leHRlbmRzKFJlbmRlckxpc3QsIF9zdXBlcik7XG4gIGZ1bmN0aW9uIFJlbmRlckxpc3QoKSB7XG4gICAgcmV0dXJuIF9zdXBlciAhPT0gbnVsbCAmJiBfc3VwZXIuYXBwbHkodGhpcywgYXJndW1lbnRzKSB8fCB0aGlzO1xuICB9XG4gIFJlbmRlckxpc3QuY3JlYXRlID0gZnVuY3Rpb24gKGFjdGlvbnMpIHtcbiAgICB2YXIgZV8xLCBfYTtcbiAgICB2YXIgbGlzdCA9IG5ldyB0aGlzKCk7XG4gICAgdHJ5IHtcbiAgICAgIGZvciAodmFyIF9iID0gX192YWx1ZXMoT2JqZWN0LmtleXMoYWN0aW9ucykpLCBfYyA9IF9iLm5leHQoKTsgIV9jLmRvbmU7IF9jID0gX2IubmV4dCgpKSB7XG4gICAgICAgIHZhciBpZCA9IF9jLnZhbHVlO1xuICAgICAgICB2YXIgX2QgPSBfX3JlYWQodGhpcy5hY3Rpb24oaWQsIGFjdGlvbnNbaWRdKSwgMiksXG4gICAgICAgICAgYWN0aW9uID0gX2RbMF0sXG4gICAgICAgICAgcHJpb3JpdHkgPSBfZFsxXTtcbiAgICAgICAgaWYgKHByaW9yaXR5KSB7XG4gICAgICAgICAgbGlzdC5hZGQoYWN0aW9uLCBwcmlvcml0eSk7XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9IGNhdGNoIChlXzFfMSkge1xuICAgICAgZV8xID0ge1xuICAgICAgICBlcnJvcjogZV8xXzFcbiAgICAgIH07XG4gICAgfSBmaW5hbGx5IHtcbiAgICAgIHRyeSB7XG4gICAgICAgIGlmIChfYyAmJiAhX2MuZG9uZSAmJiAoX2EgPSBfYi5yZXR1cm4pKSBfYS5jYWxsKF9iKTtcbiAgICAgIH0gZmluYWxseSB7XG4gICAgICAgIGlmIChlXzEpIHRocm93IGVfMS5lcnJvcjtcbiAgICAgIH1cbiAgICB9XG4gICAgcmV0dXJuIGxpc3Q7XG4gIH07XG4gIFJlbmRlckxpc3QuYWN0aW9uID0gZnVuY3Rpb24gKGlkLCBhY3Rpb24pIHtcbiAgICB2YXIgX2EsIF9iLCBfYywgX2Q7XG4gICAgdmFyIHJlbmRlckRvYywgcmVuZGVyTWF0aDtcbiAgICB2YXIgY29udmVydCA9IHRydWU7XG4gICAgdmFyIHByaW9yaXR5ID0gYWN0aW9uWzBdO1xuICAgIGlmIChhY3Rpb24ubGVuZ3RoID09PSAxIHx8IHR5cGVvZiBhY3Rpb25bMV0gPT09ICdib29sZWFuJykge1xuICAgICAgYWN0aW9uLmxlbmd0aCA9PT0gMiAmJiAoY29udmVydCA9IGFjdGlvblsxXSk7XG4gICAgICBfYSA9IF9fcmVhZCh0aGlzLm1ldGhvZEFjdGlvbnMoaWQpLCAyKSwgcmVuZGVyRG9jID0gX2FbMF0sIHJlbmRlck1hdGggPSBfYVsxXTtcbiAgICB9IGVsc2UgaWYgKHR5cGVvZiBhY3Rpb25bMV0gPT09ICdzdHJpbmcnKSB7XG4gICAgICBpZiAodHlwZW9mIGFjdGlvblsyXSA9PT0gJ3N0cmluZycpIHtcbiAgICAgICAgYWN0aW9uLmxlbmd0aCA9PT0gNCAmJiAoY29udmVydCA9IGFjdGlvblszXSk7XG4gICAgICAgIHZhciBfZSA9IF9fcmVhZChhY3Rpb24uc2xpY2UoMSksIDIpLFxuICAgICAgICAgIG1ldGhvZDEgPSBfZVswXSxcbiAgICAgICAgICBtZXRob2QyID0gX2VbMV07XG4gICAgICAgIF9iID0gX19yZWFkKHRoaXMubWV0aG9kQWN0aW9ucyhtZXRob2QxLCBtZXRob2QyKSwgMiksIHJlbmRlckRvYyA9IF9iWzBdLCByZW5kZXJNYXRoID0gX2JbMV07XG4gICAgICB9IGVsc2Uge1xuICAgICAgICBhY3Rpb24ubGVuZ3RoID09PSAzICYmIChjb252ZXJ0ID0gYWN0aW9uWzJdKTtcbiAgICAgICAgX2MgPSBfX3JlYWQodGhpcy5tZXRob2RBY3Rpb25zKGFjdGlvblsxXSksIDIpLCByZW5kZXJEb2MgPSBfY1swXSwgcmVuZGVyTWF0aCA9IF9jWzFdO1xuICAgICAgfVxuICAgIH0gZWxzZSB7XG4gICAgICBhY3Rpb24ubGVuZ3RoID09PSA0ICYmIChjb252ZXJ0ID0gYWN0aW9uWzNdKTtcbiAgICAgIF9kID0gX19yZWFkKGFjdGlvbi5zbGljZSgxKSwgMiksIHJlbmRlckRvYyA9IF9kWzBdLCByZW5kZXJNYXRoID0gX2RbMV07XG4gICAgfVxuICAgIHJldHVybiBbe1xuICAgICAgaWQ6IGlkLFxuICAgICAgcmVuZGVyRG9jOiByZW5kZXJEb2MsXG4gICAgICByZW5kZXJNYXRoOiByZW5kZXJNYXRoLFxuICAgICAgY29udmVydDogY29udmVydFxuICAgIH0sIHByaW9yaXR5XTtcbiAgfTtcbiAgUmVuZGVyTGlzdC5tZXRob2RBY3Rpb25zID0gZnVuY3Rpb24gKG1ldGhvZDEsIG1ldGhvZDIpIHtcbiAgICBpZiAobWV0aG9kMiA9PT0gdm9pZCAwKSB7XG4gICAgICBtZXRob2QyID0gbWV0aG9kMTtcbiAgICB9XG4gICAgcmV0dXJuIFtmdW5jdGlvbiAoZG9jdW1lbnQpIHtcbiAgICAgIG1ldGhvZDEgJiYgZG9jdW1lbnRbbWV0aG9kMV0oKTtcbiAgICAgIHJldHVybiBmYWxzZTtcbiAgICB9LCBmdW5jdGlvbiAobWF0aCwgZG9jdW1lbnQpIHtcbiAgICAgIG1ldGhvZDIgJiYgbWF0aFttZXRob2QyXShkb2N1bWVudCk7XG4gICAgICByZXR1cm4gZmFsc2U7XG4gICAgfV07XG4gIH07XG4gIFJlbmRlckxpc3QucHJvdG90eXBlLnJlbmRlckRvYyA9IGZ1bmN0aW9uIChkb2N1bWVudCwgc3RhcnQpIHtcbiAgICB2YXIgZV8yLCBfYTtcbiAgICBpZiAoc3RhcnQgPT09IHZvaWQgMCkge1xuICAgICAgc3RhcnQgPSBNYXRoSXRlbV9qc18xLlNUQVRFLlVOUFJPQ0VTU0VEO1xuICAgIH1cbiAgICB0cnkge1xuICAgICAgZm9yICh2YXIgX2IgPSBfX3ZhbHVlcyh0aGlzLml0ZW1zKSwgX2MgPSBfYi5uZXh0KCk7ICFfYy5kb25lOyBfYyA9IF9iLm5leHQoKSkge1xuICAgICAgICB2YXIgaXRlbSA9IF9jLnZhbHVlO1xuICAgICAgICBpZiAoaXRlbS5wcmlvcml0eSA+PSBzdGFydCkge1xuICAgICAgICAgIGlmIChpdGVtLml0ZW0ucmVuZGVyRG9jKGRvY3VtZW50KSkgcmV0dXJuO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgfSBjYXRjaCAoZV8yXzEpIHtcbiAgICAgIGVfMiA9IHtcbiAgICAgICAgZXJyb3I6IGVfMl8xXG4gICAgICB9O1xuICAgIH0gZmluYWxseSB7XG4gICAgICB0cnkge1xuICAgICAgICBpZiAoX2MgJiYgIV9jLmRvbmUgJiYgKF9hID0gX2IucmV0dXJuKSkgX2EuY2FsbChfYik7XG4gICAgICB9IGZpbmFsbHkge1xuICAgICAgICBpZiAoZV8yKSB0aHJvdyBlXzIuZXJyb3I7XG4gICAgICB9XG4gICAgfVxuICB9O1xuICBSZW5kZXJMaXN0LnByb3RvdHlwZS5yZW5kZXJNYXRoID0gZnVuY3Rpb24gKG1hdGgsIGRvY3VtZW50LCBzdGFydCkge1xuICAgIHZhciBlXzMsIF9hO1xuICAgIGlmIChzdGFydCA9PT0gdm9pZCAwKSB7XG4gICAgICBzdGFydCA9IE1hdGhJdGVtX2pzXzEuU1RBVEUuVU5QUk9DRVNTRUQ7XG4gICAgfVxuICAgIHRyeSB7XG4gICAgICBmb3IgKHZhciBfYiA9IF9fdmFsdWVzKHRoaXMuaXRlbXMpLCBfYyA9IF9iLm5leHQoKTsgIV9jLmRvbmU7IF9jID0gX2IubmV4dCgpKSB7XG4gICAgICAgIHZhciBpdGVtID0gX2MudmFsdWU7XG4gICAgICAgIGlmIChpdGVtLnByaW9yaXR5ID49IHN0YXJ0KSB7XG4gICAgICAgICAgaWYgKGl0ZW0uaXRlbS5yZW5kZXJNYXRoKG1hdGgsIGRvY3VtZW50KSkgcmV0dXJuO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgfSBjYXRjaCAoZV8zXzEpIHtcbiAgICAgIGVfMyA9IHtcbiAgICAgICAgZXJyb3I6IGVfM18xXG4gICAgICB9O1xuICAgIH0gZmluYWxseSB7XG4gICAgICB0cnkge1xuICAgICAgICBpZiAoX2MgJiYgIV9jLmRvbmUgJiYgKF9hID0gX2IucmV0dXJuKSkgX2EuY2FsbChfYik7XG4gICAgICB9IGZpbmFsbHkge1xuICAgICAgICBpZiAoZV8zKSB0aHJvdyBlXzMuZXJyb3I7XG4gICAgICB9XG4gICAgfVxuICB9O1xuICBSZW5kZXJMaXN0LnByb3RvdHlwZS5yZW5kZXJDb252ZXJ0ID0gZnVuY3Rpb24gKG1hdGgsIGRvY3VtZW50LCBlbmQpIHtcbiAgICB2YXIgZV80LCBfYTtcbiAgICBpZiAoZW5kID09PSB2b2lkIDApIHtcbiAgICAgIGVuZCA9IE1hdGhJdGVtX2pzXzEuU1RBVEUuTEFTVDtcbiAgICB9XG4gICAgdHJ5IHtcbiAgICAgIGZvciAodmFyIF9iID0gX192YWx1ZXModGhpcy5pdGVtcyksIF9jID0gX2IubmV4dCgpOyAhX2MuZG9uZTsgX2MgPSBfYi5uZXh0KCkpIHtcbiAgICAgICAgdmFyIGl0ZW0gPSBfYy52YWx1ZTtcbiAgICAgICAgaWYgKGl0ZW0ucHJpb3JpdHkgPiBlbmQpIHJldHVybjtcbiAgICAgICAgaWYgKGl0ZW0uaXRlbS5jb252ZXJ0KSB7XG4gICAgICAgICAgaWYgKGl0ZW0uaXRlbS5yZW5kZXJNYXRoKG1hdGgsIGRvY3VtZW50KSkgcmV0dXJuO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgfSBjYXRjaCAoZV80XzEpIHtcbiAgICAgIGVfNCA9IHtcbiAgICAgICAgZXJyb3I6IGVfNF8xXG4gICAgICB9O1xuICAgIH0gZmluYWxseSB7XG4gICAgICB0cnkge1xuICAgICAgICBpZiAoX2MgJiYgIV9jLmRvbmUgJiYgKF9hID0gX2IucmV0dXJuKSkgX2EuY2FsbChfYik7XG4gICAgICB9IGZpbmFsbHkge1xuICAgICAgICBpZiAoZV80KSB0aHJvdyBlXzQuZXJyb3I7XG4gICAgICB9XG4gICAgfVxuICB9O1xuICBSZW5kZXJMaXN0LnByb3RvdHlwZS5maW5kSUQgPSBmdW5jdGlvbiAoaWQpIHtcbiAgICB2YXIgZV81LCBfYTtcbiAgICB0cnkge1xuICAgICAgZm9yICh2YXIgX2IgPSBfX3ZhbHVlcyh0aGlzLml0ZW1zKSwgX2MgPSBfYi5uZXh0KCk7ICFfYy5kb25lOyBfYyA9IF9iLm5leHQoKSkge1xuICAgICAgICB2YXIgaXRlbSA9IF9jLnZhbHVlO1xuICAgICAgICBpZiAoaXRlbS5pdGVtLmlkID09PSBpZCkge1xuICAgICAgICAgIHJldHVybiBpdGVtLml0ZW07XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9IGNhdGNoIChlXzVfMSkge1xuICAgICAgZV81ID0ge1xuICAgICAgICBlcnJvcjogZV81XzFcbiAgICAgIH07XG4gICAgfSBmaW5hbGx5IHtcbiAgICAgIHRyeSB7XG4gICAgICAgIGlmIChfYyAmJiAhX2MuZG9uZSAmJiAoX2EgPSBfYi5yZXR1cm4pKSBfYS5jYWxsKF9iKTtcbiAgICAgIH0gZmluYWxseSB7XG4gICAgICAgIGlmIChlXzUpIHRocm93IGVfNS5lcnJvcjtcbiAgICAgIH1cbiAgICB9XG4gICAgcmV0dXJuIG51bGw7XG4gIH07XG4gIHJldHVybiBSZW5kZXJMaXN0O1xufShQcmlvcml0aXplZExpc3RfanNfMS5Qcmlvcml0aXplZExpc3QpO1xuZXhwb3J0cy5SZW5kZXJMaXN0ID0gUmVuZGVyTGlzdDtcbmV4cG9ydHMucmVzZXRPcHRpb25zID0ge1xuICBhbGw6IGZhbHNlLFxuICBwcm9jZXNzZWQ6IGZhbHNlLFxuICBpbnB1dEpheDogbnVsbCxcbiAgb3V0cHV0SmF4OiBudWxsXG59O1xuZXhwb3J0cy5yZXNldEFsbE9wdGlvbnMgPSB7XG4gIGFsbDogdHJ1ZSxcbiAgcHJvY2Vzc2VkOiB0cnVlLFxuICBpbnB1dEpheDogW10sXG4gIG91dHB1dEpheDogW11cbn07XG52YXIgRGVmYXVsdElucHV0SmF4ID0gZnVuY3Rpb24gKF9zdXBlcikge1xuICBfX2V4dGVuZHMoRGVmYXVsdElucHV0SmF4LCBfc3VwZXIpO1xuICBmdW5jdGlvbiBEZWZhdWx0SW5wdXRKYXgoKSB7XG4gICAgcmV0dXJuIF9zdXBlciAhPT0gbnVsbCAmJiBfc3VwZXIuYXBwbHkodGhpcywgYXJndW1lbnRzKSB8fCB0aGlzO1xuICB9XG4gIERlZmF1bHRJbnB1dEpheC5wcm90b3R5cGUuY29tcGlsZSA9IGZ1bmN0aW9uIChfbWF0aCkge1xuICAgIHJldHVybiBudWxsO1xuICB9O1xuICByZXR1cm4gRGVmYXVsdElucHV0SmF4O1xufShJbnB1dEpheF9qc18xLkFic3RyYWN0SW5wdXRKYXgpO1xudmFyIERlZmF1bHRPdXRwdXRKYXggPSBmdW5jdGlvbiAoX3N1cGVyKSB7XG4gIF9fZXh0ZW5kcyhEZWZhdWx0T3V0cHV0SmF4LCBfc3VwZXIpO1xuICBmdW5jdGlvbiBEZWZhdWx0T3V0cHV0SmF4KCkge1xuICAgIHJldHVybiBfc3VwZXIgIT09IG51bGwgJiYgX3N1cGVyLmFwcGx5KHRoaXMsIGFyZ3VtZW50cykgfHwgdGhpcztcbiAgfVxuICBEZWZhdWx0T3V0cHV0SmF4LnByb3RvdHlwZS50eXBlc2V0ID0gZnVuY3Rpb24gKF9tYXRoLCBfZG9jdW1lbnQpIHtcbiAgICBpZiAoX2RvY3VtZW50ID09PSB2b2lkIDApIHtcbiAgICAgIF9kb2N1bWVudCA9IG51bGw7XG4gICAgfVxuICAgIHJldHVybiBudWxsO1xuICB9O1xuICBEZWZhdWx0T3V0cHV0SmF4LnByb3RvdHlwZS5lc2NhcGVkID0gZnVuY3Rpb24gKF9tYXRoLCBfZG9jdW1lbnQpIHtcbiAgICByZXR1cm4gbnVsbDtcbiAgfTtcbiAgcmV0dXJuIERlZmF1bHRPdXRwdXRKYXg7XG59KE91dHB1dEpheF9qc18xLkFic3RyYWN0T3V0cHV0SmF4KTtcbnZhciBEZWZhdWx0TWF0aExpc3QgPSBmdW5jdGlvbiAoX3N1cGVyKSB7XG4gIF9fZXh0ZW5kcyhEZWZhdWx0TWF0aExpc3QsIF9zdXBlcik7XG4gIGZ1bmN0aW9uIERlZmF1bHRNYXRoTGlzdCgpIHtcbiAgICByZXR1cm4gX3N1cGVyICE9PSBudWxsICYmIF9zdXBlci5hcHBseSh0aGlzLCBhcmd1bWVudHMpIHx8IHRoaXM7XG4gIH1cbiAgcmV0dXJuIERlZmF1bHRNYXRoTGlzdDtcbn0oTWF0aExpc3RfanNfMS5BYnN0cmFjdE1hdGhMaXN0KTtcbnZhciBEZWZhdWx0TWF0aEl0ZW0gPSBmdW5jdGlvbiAoX3N1cGVyKSB7XG4gIF9fZXh0ZW5kcyhEZWZhdWx0TWF0aEl0ZW0sIF9zdXBlcik7XG4gIGZ1bmN0aW9uIERlZmF1bHRNYXRoSXRlbSgpIHtcbiAgICByZXR1cm4gX3N1cGVyICE9PSBudWxsICYmIF9zdXBlci5hcHBseSh0aGlzLCBhcmd1bWVudHMpIHx8IHRoaXM7XG4gIH1cbiAgcmV0dXJuIERlZmF1bHRNYXRoSXRlbTtcbn0oTWF0aEl0ZW1fanNfMS5BYnN0cmFjdE1hdGhJdGVtKTtcbnZhciBBYnN0cmFjdE1hdGhEb2N1bWVudCA9IGZ1bmN0aW9uICgpIHtcbiAgZnVuY3Rpb24gQWJzdHJhY3RNYXRoRG9jdW1lbnQoZG9jdW1lbnQsIGFkYXB0b3IsIG9wdGlvbnMpIHtcbiAgICB2YXIgX3RoaXMgPSB0aGlzO1xuICAgIHZhciBDTEFTUyA9IHRoaXMuY29uc3RydWN0b3I7XG4gICAgdGhpcy5kb2N1bWVudCA9IGRvY3VtZW50O1xuICAgIHRoaXMub3B0aW9ucyA9ICgwLCBPcHRpb25zX2pzXzEudXNlck9wdGlvbnMpKCgwLCBPcHRpb25zX2pzXzEuZGVmYXVsdE9wdGlvbnMpKHt9LCBDTEFTUy5PUFRJT05TKSwgb3B0aW9ucyk7XG4gICAgdGhpcy5tYXRoID0gbmV3ICh0aGlzLm9wdGlvbnNbJ01hdGhMaXN0J10gfHwgRGVmYXVsdE1hdGhMaXN0KSgpO1xuICAgIHRoaXMucmVuZGVyQWN0aW9ucyA9IFJlbmRlckxpc3QuY3JlYXRlKHRoaXMub3B0aW9uc1sncmVuZGVyQWN0aW9ucyddKTtcbiAgICB0aGlzLnByb2Nlc3NlZCA9IG5ldyBBYnN0cmFjdE1hdGhEb2N1bWVudC5Qcm9jZXNzQml0cygpO1xuICAgIHRoaXMub3V0cHV0SmF4ID0gdGhpcy5vcHRpb25zWydPdXRwdXRKYXgnXSB8fCBuZXcgRGVmYXVsdE91dHB1dEpheCgpO1xuICAgIHZhciBpbnB1dEpheCA9IHRoaXMub3B0aW9uc1snSW5wdXRKYXgnXSB8fCBbbmV3IERlZmF1bHRJbnB1dEpheCgpXTtcbiAgICBpZiAoIUFycmF5LmlzQXJyYXkoaW5wdXRKYXgpKSB7XG4gICAgICBpbnB1dEpheCA9IFtpbnB1dEpheF07XG4gICAgfVxuICAgIHRoaXMuaW5wdXRKYXggPSBpbnB1dEpheDtcbiAgICB0aGlzLmFkYXB0b3IgPSBhZGFwdG9yO1xuICAgIHRoaXMub3V0cHV0SmF4LnNldEFkYXB0b3IoYWRhcHRvcik7XG4gICAgdGhpcy5pbnB1dEpheC5tYXAoZnVuY3Rpb24gKGpheCkge1xuICAgICAgcmV0dXJuIGpheC5zZXRBZGFwdG9yKGFkYXB0b3IpO1xuICAgIH0pO1xuICAgIHRoaXMubW1sRmFjdG9yeSA9IHRoaXMub3B0aW9uc1snTW1sRmFjdG9yeSddIHx8IG5ldyBNbWxGYWN0b3J5X2pzXzEuTW1sRmFjdG9yeSgpO1xuICAgIHRoaXMuaW5wdXRKYXgubWFwKGZ1bmN0aW9uIChqYXgpIHtcbiAgICAgIHJldHVybiBqYXguc2V0TW1sRmFjdG9yeShfdGhpcy5tbWxGYWN0b3J5KTtcbiAgICB9KTtcbiAgICB0aGlzLm91dHB1dEpheC5pbml0aWFsaXplKCk7XG4gICAgdGhpcy5pbnB1dEpheC5tYXAoZnVuY3Rpb24gKGpheCkge1xuICAgICAgcmV0dXJuIGpheC5pbml0aWFsaXplKCk7XG4gICAgfSk7XG4gIH1cbiAgT2JqZWN0LmRlZmluZVByb3BlcnR5KEFic3RyYWN0TWF0aERvY3VtZW50LnByb3RvdHlwZSwgXCJraW5kXCIsIHtcbiAgICBnZXQ6IGZ1bmN0aW9uICgpIHtcbiAgICAgIHJldHVybiB0aGlzLmNvbnN0cnVjdG9yLktJTkQ7XG4gICAgfSxcbiAgICBlbnVtZXJhYmxlOiBmYWxzZSxcbiAgICBjb25maWd1cmFibGU6IHRydWVcbiAgfSk7XG4gIEFic3RyYWN0TWF0aERvY3VtZW50LnByb3RvdHlwZS5hZGRSZW5kZXJBY3Rpb24gPSBmdW5jdGlvbiAoaWQpIHtcbiAgICB2YXIgYWN0aW9uID0gW107XG4gICAgZm9yICh2YXIgX2kgPSAxOyBfaSA8IGFyZ3VtZW50cy5sZW5ndGg7IF9pKyspIHtcbiAgICAgIGFjdGlvbltfaSAtIDFdID0gYXJndW1lbnRzW19pXTtcbiAgICB9XG4gICAgdmFyIF9hID0gX19yZWFkKFJlbmRlckxpc3QuYWN0aW9uKGlkLCBhY3Rpb24pLCAyKSxcbiAgICAgIGZuID0gX2FbMF0sXG4gICAgICBwID0gX2FbMV07XG4gICAgdGhpcy5yZW5kZXJBY3Rpb25zLmFkZChmbiwgcCk7XG4gIH07XG4gIEFic3RyYWN0TWF0aERvY3VtZW50LnByb3RvdHlwZS5yZW1vdmVSZW5kZXJBY3Rpb24gPSBmdW5jdGlvbiAoaWQpIHtcbiAgICB2YXIgYWN0aW9uID0gdGhpcy5yZW5kZXJBY3Rpb25zLmZpbmRJRChpZCk7XG4gICAgaWYgKGFjdGlvbikge1xuICAgICAgdGhpcy5yZW5kZXJBY3Rpb25zLnJlbW92ZShhY3Rpb24pO1xuICAgIH1cbiAgfTtcbiAgQWJzdHJhY3RNYXRoRG9jdW1lbnQucHJvdG90eXBlLnJlbmRlciA9IGZ1bmN0aW9uICgpIHtcbiAgICB0aGlzLnJlbmRlckFjdGlvbnMucmVuZGVyRG9jKHRoaXMpO1xuICAgIHJldHVybiB0aGlzO1xuICB9O1xuICBBYnN0cmFjdE1hdGhEb2N1bWVudC5wcm90b3R5cGUucmVyZW5kZXIgPSBmdW5jdGlvbiAoc3RhcnQpIHtcbiAgICBpZiAoc3RhcnQgPT09IHZvaWQgMCkge1xuICAgICAgc3RhcnQgPSBNYXRoSXRlbV9qc18xLlNUQVRFLlJFUkVOREVSO1xuICAgIH1cbiAgICB0aGlzLnN0YXRlKHN0YXJ0IC0gMSk7XG4gICAgdGhpcy5yZW5kZXIoKTtcbiAgICByZXR1cm4gdGhpcztcbiAgfTtcbiAgQWJzdHJhY3RNYXRoRG9jdW1lbnQucHJvdG90eXBlLmNvbnZlcnQgPSBmdW5jdGlvbiAobWF0aCwgb3B0aW9ucykge1xuICAgIGlmIChvcHRpb25zID09PSB2b2lkIDApIHtcbiAgICAgIG9wdGlvbnMgPSB7fTtcbiAgICB9XG4gICAgdmFyIF9hID0gKDAsIE9wdGlvbnNfanNfMS51c2VyT3B0aW9ucykoe1xuICAgICAgICBmb3JtYXQ6IHRoaXMuaW5wdXRKYXhbMF0ubmFtZSxcbiAgICAgICAgZGlzcGxheTogdHJ1ZSxcbiAgICAgICAgZW5kOiBNYXRoSXRlbV9qc18xLlNUQVRFLkxBU1QsXG4gICAgICAgIGVtOiAxNixcbiAgICAgICAgZXg6IDgsXG4gICAgICAgIGNvbnRhaW5lcldpZHRoOiBudWxsLFxuICAgICAgICBsaW5lV2lkdGg6IDEwMDAwMDAsXG4gICAgICAgIHNjYWxlOiAxLFxuICAgICAgICBmYW1pbHk6ICcnXG4gICAgICB9LCBvcHRpb25zKSxcbiAgICAgIGZvcm1hdCA9IF9hLmZvcm1hdCxcbiAgICAgIGRpc3BsYXkgPSBfYS5kaXNwbGF5LFxuICAgICAgZW5kID0gX2EuZW5kLFxuICAgICAgZXggPSBfYS5leCxcbiAgICAgIGVtID0gX2EuZW0sXG4gICAgICBjb250YWluZXJXaWR0aCA9IF9hLmNvbnRhaW5lcldpZHRoLFxuICAgICAgbGluZVdpZHRoID0gX2EubGluZVdpZHRoLFxuICAgICAgc2NhbGUgPSBfYS5zY2FsZSxcbiAgICAgIGZhbWlseSA9IF9hLmZhbWlseTtcbiAgICBpZiAoY29udGFpbmVyV2lkdGggPT09IG51bGwpIHtcbiAgICAgIGNvbnRhaW5lcldpZHRoID0gODAgKiBleDtcbiAgICB9XG4gICAgdmFyIGpheCA9IHRoaXMuaW5wdXRKYXgucmVkdWNlKGZ1bmN0aW9uIChqYXgsIGlqYXgpIHtcbiAgICAgIHJldHVybiBpamF4Lm5hbWUgPT09IGZvcm1hdCA/IGlqYXggOiBqYXg7XG4gICAgfSwgbnVsbCk7XG4gICAgdmFyIG1pdGVtID0gbmV3IHRoaXMub3B0aW9ucy5NYXRoSXRlbShtYXRoLCBqYXgsIGRpc3BsYXkpO1xuICAgIG1pdGVtLnN0YXJ0Lm5vZGUgPSB0aGlzLmFkYXB0b3IuYm9keSh0aGlzLmRvY3VtZW50KTtcbiAgICBtaXRlbS5zZXRNZXRyaWNzKGVtLCBleCwgY29udGFpbmVyV2lkdGgsIGxpbmVXaWR0aCwgc2NhbGUpO1xuICAgIGlmICh0aGlzLm91dHB1dEpheC5vcHRpb25zLm10ZXh0SW5oZXJpdEZvbnQpIHtcbiAgICAgIG1pdGVtLm91dHB1dERhdGEubXRleHRGYW1pbHkgPSBmYW1pbHk7XG4gICAgfVxuICAgIGlmICh0aGlzLm91dHB1dEpheC5vcHRpb25zLm1lcnJvckluaGVyaXRGb250KSB7XG4gICAgICBtaXRlbS5vdXRwdXREYXRhLm1lcnJvckZhbWlseSA9IGZhbWlseTtcbiAgICB9XG4gICAgbWl0ZW0uY29udmVydCh0aGlzLCBlbmQpO1xuICAgIHJldHVybiBtaXRlbS50eXBlc2V0Um9vdCB8fCBtaXRlbS5yb290O1xuICB9O1xuICBBYnN0cmFjdE1hdGhEb2N1bWVudC5wcm90b3R5cGUuZmluZE1hdGggPSBmdW5jdGlvbiAoX29wdGlvbnMpIHtcbiAgICBpZiAoX29wdGlvbnMgPT09IHZvaWQgMCkge1xuICAgICAgX29wdGlvbnMgPSBudWxsO1xuICAgIH1cbiAgICB0aGlzLnByb2Nlc3NlZC5zZXQoJ2ZpbmRNYXRoJyk7XG4gICAgcmV0dXJuIHRoaXM7XG4gIH07XG4gIEFic3RyYWN0TWF0aERvY3VtZW50LnByb3RvdHlwZS5jb21waWxlID0gZnVuY3Rpb24gKCkge1xuICAgIHZhciBlXzYsIF9hLCBlXzcsIF9iO1xuICAgIGlmICghdGhpcy5wcm9jZXNzZWQuaXNTZXQoJ2NvbXBpbGUnKSkge1xuICAgICAgdmFyIHJlY29tcGlsZSA9IFtdO1xuICAgICAgdHJ5IHtcbiAgICAgICAgZm9yICh2YXIgX2MgPSBfX3ZhbHVlcyh0aGlzLm1hdGgpLCBfZCA9IF9jLm5leHQoKTsgIV9kLmRvbmU7IF9kID0gX2MubmV4dCgpKSB7XG4gICAgICAgICAgdmFyIG1hdGggPSBfZC52YWx1ZTtcbiAgICAgICAgICB0aGlzLmNvbXBpbGVNYXRoKG1hdGgpO1xuICAgICAgICAgIGlmIChtYXRoLmlucHV0RGF0YS5yZWNvbXBpbGUgIT09IHVuZGVmaW5lZCkge1xuICAgICAgICAgICAgcmVjb21waWxlLnB1c2gobWF0aCk7XG4gICAgICAgICAgfVxuICAgICAgICB9XG4gICAgICB9IGNhdGNoIChlXzZfMSkge1xuICAgICAgICBlXzYgPSB7XG4gICAgICAgICAgZXJyb3I6IGVfNl8xXG4gICAgICAgIH07XG4gICAgICB9IGZpbmFsbHkge1xuICAgICAgICB0cnkge1xuICAgICAgICAgIGlmIChfZCAmJiAhX2QuZG9uZSAmJiAoX2EgPSBfYy5yZXR1cm4pKSBfYS5jYWxsKF9jKTtcbiAgICAgICAgfSBmaW5hbGx5IHtcbiAgICAgICAgICBpZiAoZV82KSB0aHJvdyBlXzYuZXJyb3I7XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICAgIHRyeSB7XG4gICAgICAgIGZvciAodmFyIHJlY29tcGlsZV8xID0gX192YWx1ZXMocmVjb21waWxlKSwgcmVjb21waWxlXzFfMSA9IHJlY29tcGlsZV8xLm5leHQoKTsgIXJlY29tcGlsZV8xXzEuZG9uZTsgcmVjb21waWxlXzFfMSA9IHJlY29tcGlsZV8xLm5leHQoKSkge1xuICAgICAgICAgIHZhciBtYXRoID0gcmVjb21waWxlXzFfMS52YWx1ZTtcbiAgICAgICAgICB2YXIgZGF0YSA9IG1hdGguaW5wdXREYXRhLnJlY29tcGlsZTtcbiAgICAgICAgICBtYXRoLnN0YXRlKGRhdGEuc3RhdGUpO1xuICAgICAgICAgIG1hdGguaW5wdXREYXRhLnJlY29tcGlsZSA9IGRhdGE7XG4gICAgICAgICAgdGhpcy5jb21waWxlTWF0aChtYXRoKTtcbiAgICAgICAgfVxuICAgICAgfSBjYXRjaCAoZV83XzEpIHtcbiAgICAgICAgZV83ID0ge1xuICAgICAgICAgIGVycm9yOiBlXzdfMVxuICAgICAgICB9O1xuICAgICAgfSBmaW5hbGx5IHtcbiAgICAgICAgdHJ5IHtcbiAgICAgICAgICBpZiAocmVjb21waWxlXzFfMSAmJiAhcmVjb21waWxlXzFfMS5kb25lICYmIChfYiA9IHJlY29tcGlsZV8xLnJldHVybikpIF9iLmNhbGwocmVjb21waWxlXzEpO1xuICAgICAgICB9IGZpbmFsbHkge1xuICAgICAgICAgIGlmIChlXzcpIHRocm93IGVfNy5lcnJvcjtcbiAgICAgICAgfVxuICAgICAgfVxuICAgICAgdGhpcy5wcm9jZXNzZWQuc2V0KCdjb21waWxlJyk7XG4gICAgfVxuICAgIHJldHVybiB0aGlzO1xuICB9O1xuICBBYnN0cmFjdE1hdGhEb2N1bWVudC5wcm90b3R5cGUuY29tcGlsZU1hdGggPSBmdW5jdGlvbiAobWF0aCkge1xuICAgIHRyeSB7XG4gICAgICBtYXRoLmNvbXBpbGUodGhpcyk7XG4gICAgfSBjYXRjaCAoZXJyKSB7XG4gICAgICBpZiAoZXJyLnJldHJ5IHx8IGVyci5yZXN0YXJ0KSB7XG4gICAgICAgIHRocm93IGVycjtcbiAgICAgIH1cbiAgICAgIHRoaXMub3B0aW9uc1snY29tcGlsZUVycm9yJ10odGhpcywgbWF0aCwgZXJyKTtcbiAgICAgIG1hdGguaW5wdXREYXRhWydlcnJvciddID0gZXJyO1xuICAgIH1cbiAgfTtcbiAgQWJzdHJhY3RNYXRoRG9jdW1lbnQucHJvdG90eXBlLmNvbXBpbGVFcnJvciA9IGZ1bmN0aW9uIChtYXRoLCBlcnIpIHtcbiAgICBtYXRoLnJvb3QgPSB0aGlzLm1tbEZhY3RvcnkuY3JlYXRlKCdtYXRoJywgbnVsbCwgW3RoaXMubW1sRmFjdG9yeS5jcmVhdGUoJ21lcnJvcicsIHtcbiAgICAgICdkYXRhLW1qeC1lcnJvcic6IGVyci5tZXNzYWdlLFxuICAgICAgdGl0bGU6IGVyci5tZXNzYWdlXG4gICAgfSwgW3RoaXMubW1sRmFjdG9yeS5jcmVhdGUoJ210ZXh0JywgbnVsbCwgW3RoaXMubW1sRmFjdG9yeS5jcmVhdGUoJ3RleHQnKS5zZXRUZXh0KCdNYXRoIGlucHV0IGVycm9yJyldKV0pXSk7XG4gICAgaWYgKG1hdGguZGlzcGxheSkge1xuICAgICAgbWF0aC5yb290LmF0dHJpYnV0ZXMuc2V0KCdkaXNwbGF5JywgJ2Jsb2NrJyk7XG4gICAgfVxuICAgIG1hdGguaW5wdXREYXRhLmVycm9yID0gZXJyLm1lc3NhZ2U7XG4gIH07XG4gIEFic3RyYWN0TWF0aERvY3VtZW50LnByb3RvdHlwZS50eXBlc2V0ID0gZnVuY3Rpb24gKCkge1xuICAgIHZhciBlXzgsIF9hO1xuICAgIGlmICghdGhpcy5wcm9jZXNzZWQuaXNTZXQoJ3R5cGVzZXQnKSkge1xuICAgICAgdHJ5IHtcbiAgICAgICAgZm9yICh2YXIgX2IgPSBfX3ZhbHVlcyh0aGlzLm1hdGgpLCBfYyA9IF9iLm5leHQoKTsgIV9jLmRvbmU7IF9jID0gX2IubmV4dCgpKSB7XG4gICAgICAgICAgdmFyIG1hdGggPSBfYy52YWx1ZTtcbiAgICAgICAgICB0cnkge1xuICAgICAgICAgICAgbWF0aC50eXBlc2V0KHRoaXMpO1xuICAgICAgICAgIH0gY2F0Y2ggKGVycikge1xuICAgICAgICAgICAgaWYgKGVyci5yZXRyeSB8fCBlcnIucmVzdGFydCkge1xuICAgICAgICAgICAgICB0aHJvdyBlcnI7XG4gICAgICAgICAgICB9XG4gICAgICAgICAgICB0aGlzLm9wdGlvbnNbJ3R5cGVzZXRFcnJvciddKHRoaXMsIG1hdGgsIGVycik7XG4gICAgICAgICAgICBtYXRoLm91dHB1dERhdGFbJ2Vycm9yJ10gPSBlcnI7XG4gICAgICAgICAgfVxuICAgICAgICB9XG4gICAgICB9IGNhdGNoIChlXzhfMSkge1xuICAgICAgICBlXzggPSB7XG4gICAgICAgICAgZXJyb3I6IGVfOF8xXG4gICAgICAgIH07XG4gICAgICB9IGZpbmFsbHkge1xuICAgICAgICB0cnkge1xuICAgICAgICAgIGlmIChfYyAmJiAhX2MuZG9uZSAmJiAoX2EgPSBfYi5yZXR1cm4pKSBfYS5jYWxsKF9iKTtcbiAgICAgICAgfSBmaW5hbGx5IHtcbiAgICAgICAgICBpZiAoZV84KSB0aHJvdyBlXzguZXJyb3I7XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICAgIHRoaXMucHJvY2Vzc2VkLnNldCgndHlwZXNldCcpO1xuICAgIH1cbiAgICByZXR1cm4gdGhpcztcbiAgfTtcbiAgQWJzdHJhY3RNYXRoRG9jdW1lbnQucHJvdG90eXBlLnR5cGVzZXRFcnJvciA9IGZ1bmN0aW9uIChtYXRoLCBlcnIpIHtcbiAgICBtYXRoLnR5cGVzZXRSb290ID0gdGhpcy5hZGFwdG9yLm5vZGUoJ21qeC1jb250YWluZXInLCB7XG4gICAgICBjbGFzczogJ01hdGhKYXggbWp4LW91dHB1dC1lcnJvcicsXG4gICAgICBqYXg6IHRoaXMub3V0cHV0SmF4Lm5hbWVcbiAgICB9LCBbdGhpcy5hZGFwdG9yLm5vZGUoJ3NwYW4nLCB7XG4gICAgICAnZGF0YS1tangtZXJyb3InOiBlcnIubWVzc2FnZSxcbiAgICAgIHRpdGxlOiBlcnIubWVzc2FnZSxcbiAgICAgIHN0eWxlOiB7XG4gICAgICAgIGNvbG9yOiAncmVkJyxcbiAgICAgICAgJ2JhY2tncm91bmQtY29sb3InOiAneWVsbG93JyxcbiAgICAgICAgJ2xpbmUtaGVpZ2h0JzogJ25vcm1hbCdcbiAgICAgIH1cbiAgICB9LCBbdGhpcy5hZGFwdG9yLnRleHQoJ01hdGggb3V0cHV0IGVycm9yJyldKV0pO1xuICAgIGlmIChtYXRoLmRpc3BsYXkpIHtcbiAgICAgIHRoaXMuYWRhcHRvci5zZXRBdHRyaWJ1dGVzKG1hdGgudHlwZXNldFJvb3QsIHtcbiAgICAgICAgc3R5bGU6IHtcbiAgICAgICAgICBkaXNwbGF5OiAnYmxvY2snLFxuICAgICAgICAgIG1hcmdpbjogJzFlbSAwJyxcbiAgICAgICAgICAndGV4dC1hbGlnbic6ICdjZW50ZXInXG4gICAgICAgIH1cbiAgICAgIH0pO1xuICAgIH1cbiAgICBtYXRoLm91dHB1dERhdGEuZXJyb3IgPSBlcnIubWVzc2FnZTtcbiAgfTtcbiAgQWJzdHJhY3RNYXRoRG9jdW1lbnQucHJvdG90eXBlLmdldE1ldHJpY3MgPSBmdW5jdGlvbiAoKSB7XG4gICAgaWYgKCF0aGlzLnByb2Nlc3NlZC5pc1NldCgnZ2V0TWV0cmljcycpKSB7XG4gICAgICB0aGlzLm91dHB1dEpheC5nZXRNZXRyaWNzKHRoaXMpO1xuICAgICAgdGhpcy5wcm9jZXNzZWQuc2V0KCdnZXRNZXRyaWNzJyk7XG4gICAgfVxuICAgIHJldHVybiB0aGlzO1xuICB9O1xuICBBYnN0cmFjdE1hdGhEb2N1bWVudC5wcm90b3R5cGUudXBkYXRlRG9jdW1lbnQgPSBmdW5jdGlvbiAoKSB7XG4gICAgdmFyIGVfOSwgX2E7XG4gICAgaWYgKCF0aGlzLnByb2Nlc3NlZC5pc1NldCgndXBkYXRlRG9jdW1lbnQnKSkge1xuICAgICAgdHJ5IHtcbiAgICAgICAgZm9yICh2YXIgX2IgPSBfX3ZhbHVlcyh0aGlzLm1hdGgucmV2ZXJzZWQoKSksIF9jID0gX2IubmV4dCgpOyAhX2MuZG9uZTsgX2MgPSBfYi5uZXh0KCkpIHtcbiAgICAgICAgICB2YXIgbWF0aCA9IF9jLnZhbHVlO1xuICAgICAgICAgIG1hdGgudXBkYXRlRG9jdW1lbnQodGhpcyk7XG4gICAgICAgIH1cbiAgICAgIH0gY2F0Y2ggKGVfOV8xKSB7XG4gICAgICAgIGVfOSA9IHtcbiAgICAgICAgICBlcnJvcjogZV85XzFcbiAgICAgICAgfTtcbiAgICAgIH0gZmluYWxseSB7XG4gICAgICAgIHRyeSB7XG4gICAgICAgICAgaWYgKF9jICYmICFfYy5kb25lICYmIChfYSA9IF9iLnJldHVybikpIF9hLmNhbGwoX2IpO1xuICAgICAgICB9IGZpbmFsbHkge1xuICAgICAgICAgIGlmIChlXzkpIHRocm93IGVfOS5lcnJvcjtcbiAgICAgICAgfVxuICAgICAgfVxuICAgICAgdGhpcy5wcm9jZXNzZWQuc2V0KCd1cGRhdGVEb2N1bWVudCcpO1xuICAgIH1cbiAgICByZXR1cm4gdGhpcztcbiAgfTtcbiAgQWJzdHJhY3RNYXRoRG9jdW1lbnQucHJvdG90eXBlLnJlbW92ZUZyb21Eb2N1bWVudCA9IGZ1bmN0aW9uIChfcmVzdG9yZSkge1xuICAgIGlmIChfcmVzdG9yZSA9PT0gdm9pZCAwKSB7XG4gICAgICBfcmVzdG9yZSA9IGZhbHNlO1xuICAgIH1cbiAgICByZXR1cm4gdGhpcztcbiAgfTtcbiAgQWJzdHJhY3RNYXRoRG9jdW1lbnQucHJvdG90eXBlLnN0YXRlID0gZnVuY3Rpb24gKHN0YXRlLCByZXN0b3JlKSB7XG4gICAgdmFyIGVfMTAsIF9hO1xuICAgIGlmIChyZXN0b3JlID09PSB2b2lkIDApIHtcbiAgICAgIHJlc3RvcmUgPSBmYWxzZTtcbiAgICB9XG4gICAgdHJ5IHtcbiAgICAgIGZvciAodmFyIF9iID0gX192YWx1ZXModGhpcy5tYXRoKSwgX2MgPSBfYi5uZXh0KCk7ICFfYy5kb25lOyBfYyA9IF9iLm5leHQoKSkge1xuICAgICAgICB2YXIgbWF0aCA9IF9jLnZhbHVlO1xuICAgICAgICBtYXRoLnN0YXRlKHN0YXRlLCByZXN0b3JlKTtcbiAgICAgIH1cbiAgICB9IGNhdGNoIChlXzEwXzEpIHtcbiAgICAgIGVfMTAgPSB7XG4gICAgICAgIGVycm9yOiBlXzEwXzFcbiAgICAgIH07XG4gICAgfSBmaW5hbGx5IHtcbiAgICAgIHRyeSB7XG4gICAgICAgIGlmIChfYyAmJiAhX2MuZG9uZSAmJiAoX2EgPSBfYi5yZXR1cm4pKSBfYS5jYWxsKF9iKTtcbiAgICAgIH0gZmluYWxseSB7XG4gICAgICAgIGlmIChlXzEwKSB0aHJvdyBlXzEwLmVycm9yO1xuICAgICAgfVxuICAgIH1cbiAgICBpZiAoc3RhdGUgPCBNYXRoSXRlbV9qc18xLlNUQVRFLklOU0VSVEVEKSB7XG4gICAgICB0aGlzLnByb2Nlc3NlZC5jbGVhcigndXBkYXRlRG9jdW1lbnQnKTtcbiAgICB9XG4gICAgaWYgKHN0YXRlIDwgTWF0aEl0ZW1fanNfMS5TVEFURS5UWVBFU0VUKSB7XG4gICAgICB0aGlzLnByb2Nlc3NlZC5jbGVhcigndHlwZXNldCcpO1xuICAgICAgdGhpcy5wcm9jZXNzZWQuY2xlYXIoJ2dldE1ldHJpY3MnKTtcbiAgICB9XG4gICAgaWYgKHN0YXRlIDwgTWF0aEl0ZW1fanNfMS5TVEFURS5DT01QSUxFRCkge1xuICAgICAgdGhpcy5wcm9jZXNzZWQuY2xlYXIoJ2NvbXBpbGUnKTtcbiAgICB9XG4gICAgcmV0dXJuIHRoaXM7XG4gIH07XG4gIEFic3RyYWN0TWF0aERvY3VtZW50LnByb3RvdHlwZS5yZXNldCA9IGZ1bmN0aW9uIChvcHRpb25zKSB7XG4gICAgdmFyIF9hO1xuICAgIGlmIChvcHRpb25zID09PSB2b2lkIDApIHtcbiAgICAgIG9wdGlvbnMgPSB7XG4gICAgICAgIHByb2Nlc3NlZDogdHJ1ZVxuICAgICAgfTtcbiAgICB9XG4gICAgb3B0aW9ucyA9ICgwLCBPcHRpb25zX2pzXzEudXNlck9wdGlvbnMpKE9iamVjdC5hc3NpZ24oe30sIGV4cG9ydHMucmVzZXRPcHRpb25zKSwgb3B0aW9ucyk7XG4gICAgb3B0aW9ucy5hbGwgJiYgT2JqZWN0LmFzc2lnbihvcHRpb25zLCBleHBvcnRzLnJlc2V0QWxsT3B0aW9ucyk7XG4gICAgb3B0aW9ucy5wcm9jZXNzZWQgJiYgdGhpcy5wcm9jZXNzZWQucmVzZXQoKTtcbiAgICBvcHRpb25zLmlucHV0SmF4ICYmIHRoaXMuaW5wdXRKYXguZm9yRWFjaChmdW5jdGlvbiAoamF4KSB7XG4gICAgICByZXR1cm4gamF4LnJlc2V0LmFwcGx5KGpheCwgX19zcHJlYWRBcnJheShbXSwgX19yZWFkKG9wdGlvbnMuaW5wdXRKYXgpLCBmYWxzZSkpO1xuICAgIH0pO1xuICAgIG9wdGlvbnMub3V0cHV0SmF4ICYmIChfYSA9IHRoaXMub3V0cHV0SmF4KS5yZXNldC5hcHBseShfYSwgX19zcHJlYWRBcnJheShbXSwgX19yZWFkKG9wdGlvbnMub3V0cHV0SmF4KSwgZmFsc2UpKTtcbiAgICByZXR1cm4gdGhpcztcbiAgfTtcbiAgQWJzdHJhY3RNYXRoRG9jdW1lbnQucHJvdG90eXBlLmNsZWFyID0gZnVuY3Rpb24gKCkge1xuICAgIHRoaXMucmVzZXQoKTtcbiAgICB0aGlzLm1hdGguY2xlYXIoKTtcbiAgICByZXR1cm4gdGhpcztcbiAgfTtcbiAgQWJzdHJhY3RNYXRoRG9jdW1lbnQucHJvdG90eXBlLmNvbmNhdCA9IGZ1bmN0aW9uIChsaXN0KSB7XG4gICAgdGhpcy5tYXRoLm1lcmdlKGxpc3QpO1xuICAgIHJldHVybiB0aGlzO1xuICB9O1xuICBBYnN0cmFjdE1hdGhEb2N1bWVudC5wcm90b3R5cGUuY2xlYXJNYXRoSXRlbXNXaXRoaW4gPSBmdW5jdGlvbiAoY29udGFpbmVycykge1xuICAgIHZhciBfYTtcbiAgICB2YXIgaXRlbXMgPSB0aGlzLmdldE1hdGhJdGVtc1dpdGhpbihjb250YWluZXJzKTtcbiAgICAoX2EgPSB0aGlzLm1hdGgpLnJlbW92ZS5hcHBseShfYSwgX19zcHJlYWRBcnJheShbXSwgX19yZWFkKGl0ZW1zKSwgZmFsc2UpKTtcbiAgICByZXR1cm4gaXRlbXM7XG4gIH07XG4gIEFic3RyYWN0TWF0aERvY3VtZW50LnByb3RvdHlwZS5nZXRNYXRoSXRlbXNXaXRoaW4gPSBmdW5jdGlvbiAoZWxlbWVudHMpIHtcbiAgICB2YXIgZV8xMSwgX2EsIGVfMTIsIF9iO1xuICAgIGlmICghQXJyYXkuaXNBcnJheShlbGVtZW50cykpIHtcbiAgICAgIGVsZW1lbnRzID0gW2VsZW1lbnRzXTtcbiAgICB9XG4gICAgdmFyIGFkYXB0b3IgPSB0aGlzLmFkYXB0b3I7XG4gICAgdmFyIGl0ZW1zID0gW107XG4gICAgdmFyIGNvbnRhaW5lcnMgPSBhZGFwdG9yLmdldEVsZW1lbnRzKGVsZW1lbnRzLCB0aGlzLmRvY3VtZW50KTtcbiAgICB0cnkge1xuICAgICAgSVRFTVM6IGZvciAodmFyIF9jID0gX192YWx1ZXModGhpcy5tYXRoKSwgX2QgPSBfYy5uZXh0KCk7ICFfZC5kb25lOyBfZCA9IF9jLm5leHQoKSkge1xuICAgICAgICB2YXIgaXRlbSA9IF9kLnZhbHVlO1xuICAgICAgICB0cnkge1xuICAgICAgICAgIGZvciAodmFyIGNvbnRhaW5lcnNfMSA9IChlXzEyID0gdm9pZCAwLCBfX3ZhbHVlcyhjb250YWluZXJzKSksIGNvbnRhaW5lcnNfMV8xID0gY29udGFpbmVyc18xLm5leHQoKTsgIWNvbnRhaW5lcnNfMV8xLmRvbmU7IGNvbnRhaW5lcnNfMV8xID0gY29udGFpbmVyc18xLm5leHQoKSkge1xuICAgICAgICAgICAgdmFyIGNvbnRhaW5lciA9IGNvbnRhaW5lcnNfMV8xLnZhbHVlO1xuICAgICAgICAgICAgaWYgKGl0ZW0uc3RhcnQubm9kZSAmJiBhZGFwdG9yLmNvbnRhaW5zKGNvbnRhaW5lciwgaXRlbS5zdGFydC5ub2RlKSkge1xuICAgICAgICAgICAgICBpdGVtcy5wdXNoKGl0ZW0pO1xuICAgICAgICAgICAgICBjb250aW51ZSBJVEVNUztcbiAgICAgICAgICAgIH1cbiAgICAgICAgICB9XG4gICAgICAgIH0gY2F0Y2ggKGVfMTJfMSkge1xuICAgICAgICAgIGVfMTIgPSB7XG4gICAgICAgICAgICBlcnJvcjogZV8xMl8xXG4gICAgICAgICAgfTtcbiAgICAgICAgfSBmaW5hbGx5IHtcbiAgICAgICAgICB0cnkge1xuICAgICAgICAgICAgaWYgKGNvbnRhaW5lcnNfMV8xICYmICFjb250YWluZXJzXzFfMS5kb25lICYmIChfYiA9IGNvbnRhaW5lcnNfMS5yZXR1cm4pKSBfYi5jYWxsKGNvbnRhaW5lcnNfMSk7XG4gICAgICAgICAgfSBmaW5hbGx5IHtcbiAgICAgICAgICAgIGlmIChlXzEyKSB0aHJvdyBlXzEyLmVycm9yO1xuICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgICAgfVxuICAgIH0gY2F0Y2ggKGVfMTFfMSkge1xuICAgICAgZV8xMSA9IHtcbiAgICAgICAgZXJyb3I6IGVfMTFfMVxuICAgICAgfTtcbiAgICB9IGZpbmFsbHkge1xuICAgICAgdHJ5IHtcbiAgICAgICAgaWYgKF9kICYmICFfZC5kb25lICYmIChfYSA9IF9jLnJldHVybikpIF9hLmNhbGwoX2MpO1xuICAgICAgfSBmaW5hbGx5IHtcbiAgICAgICAgaWYgKGVfMTEpIHRocm93IGVfMTEuZXJyb3I7XG4gICAgICB9XG4gICAgfVxuICAgIHJldHVybiBpdGVtcztcbiAgfTtcbiAgQWJzdHJhY3RNYXRoRG9jdW1lbnQuS0lORCA9ICdNYXRoRG9jdW1lbnQnO1xuICBBYnN0cmFjdE1hdGhEb2N1bWVudC5PUFRJT05TID0ge1xuICAgIE91dHB1dEpheDogbnVsbCxcbiAgICBJbnB1dEpheDogbnVsbCxcbiAgICBNbWxGYWN0b3J5OiBudWxsLFxuICAgIE1hdGhMaXN0OiBEZWZhdWx0TWF0aExpc3QsXG4gICAgTWF0aEl0ZW06IERlZmF1bHRNYXRoSXRlbSxcbiAgICBjb21waWxlRXJyb3I6IGZ1bmN0aW9uIChkb2MsIG1hdGgsIGVycikge1xuICAgICAgZG9jLmNvbXBpbGVFcnJvcihtYXRoLCBlcnIpO1xuICAgIH0sXG4gICAgdHlwZXNldEVycm9yOiBmdW5jdGlvbiAoZG9jLCBtYXRoLCBlcnIpIHtcbiAgICAgIGRvYy50eXBlc2V0RXJyb3IobWF0aCwgZXJyKTtcbiAgICB9LFxuICAgIHJlbmRlckFjdGlvbnM6ICgwLCBPcHRpb25zX2pzXzEuZXhwYW5kYWJsZSkoe1xuICAgICAgZmluZDogW01hdGhJdGVtX2pzXzEuU1RBVEUuRklORE1BVEgsICdmaW5kTWF0aCcsICcnLCBmYWxzZV0sXG4gICAgICBjb21waWxlOiBbTWF0aEl0ZW1fanNfMS5TVEFURS5DT01QSUxFRF0sXG4gICAgICBtZXRyaWNzOiBbTWF0aEl0ZW1fanNfMS5TVEFURS5NRVRSSUNTLCAnZ2V0TWV0cmljcycsICcnLCBmYWxzZV0sXG4gICAgICB0eXBlc2V0OiBbTWF0aEl0ZW1fanNfMS5TVEFURS5UWVBFU0VUXSxcbiAgICAgIHVwZGF0ZTogW01hdGhJdGVtX2pzXzEuU1RBVEUuSU5TRVJURUQsICd1cGRhdGVEb2N1bWVudCcsIGZhbHNlXVxuICAgIH0pXG4gIH07XG4gIEFic3RyYWN0TWF0aERvY3VtZW50LlByb2Nlc3NCaXRzID0gKDAsIEJpdEZpZWxkX2pzXzEuQml0RmllbGRDbGFzcykoJ2ZpbmRNYXRoJywgJ2NvbXBpbGUnLCAnZ2V0TWV0cmljcycsICd0eXBlc2V0JywgJ3VwZGF0ZURvY3VtZW50Jyk7XG4gIHJldHVybiBBYnN0cmFjdE1hdGhEb2N1bWVudDtcbn0oKTtcbmV4cG9ydHMuQWJzdHJhY3RNYXRoRG9jdW1lbnQgPSBBYnN0cmFjdE1hdGhEb2N1bWVudDsiLCJcInVzZSBzdHJpY3RcIjtcblxudmFyIF9fZXh0ZW5kcyA9IHRoaXMgJiYgdGhpcy5fX2V4dGVuZHMgfHwgZnVuY3Rpb24gKCkge1xuICB2YXIgZXh0ZW5kU3RhdGljcyA9IGZ1bmN0aW9uIChkLCBiKSB7XG4gICAgZXh0ZW5kU3RhdGljcyA9IE9iamVjdC5zZXRQcm90b3R5cGVPZiB8fCB7XG4gICAgICBfX3Byb3RvX186IFtdXG4gICAgfSBpbnN0YW5jZW9mIEFycmF5ICYmIGZ1bmN0aW9uIChkLCBiKSB7XG4gICAgICBkLl9fcHJvdG9fXyA9IGI7XG4gICAgfSB8fCBmdW5jdGlvbiAoZCwgYikge1xuICAgICAgZm9yICh2YXIgcCBpbiBiKSBpZiAoT2JqZWN0LnByb3RvdHlwZS5oYXNPd25Qcm9wZXJ0eS5jYWxsKGIsIHApKSBkW3BdID0gYltwXTtcbiAgICB9O1xuICAgIHJldHVybiBleHRlbmRTdGF0aWNzKGQsIGIpO1xuICB9O1xuICByZXR1cm4gZnVuY3Rpb24gKGQsIGIpIHtcbiAgICBpZiAodHlwZW9mIGIgIT09IFwiZnVuY3Rpb25cIiAmJiBiICE9PSBudWxsKSB0aHJvdyBuZXcgVHlwZUVycm9yKFwiQ2xhc3MgZXh0ZW5kcyB2YWx1ZSBcIiArIFN0cmluZyhiKSArIFwiIGlzIG5vdCBhIGNvbnN0cnVjdG9yIG9yIG51bGxcIik7XG4gICAgZXh0ZW5kU3RhdGljcyhkLCBiKTtcbiAgICBmdW5jdGlvbiBfXygpIHtcbiAgICAgIHRoaXMuY29uc3RydWN0b3IgPSBkO1xuICAgIH1cbiAgICBkLnByb3RvdHlwZSA9IGIgPT09IG51bGwgPyBPYmplY3QuY3JlYXRlKGIpIDogKF9fLnByb3RvdHlwZSA9IGIucHJvdG90eXBlLCBuZXcgX18oKSk7XG4gIH07XG59KCk7XG5PYmplY3QuZGVmaW5lUHJvcGVydHkoZXhwb3J0cywgXCJfX2VzTW9kdWxlXCIsIHtcbiAgdmFsdWU6IHRydWVcbn0pO1xuZXhwb3J0cy5BYnN0cmFjdE1hdGhMaXN0ID0gdm9pZCAwO1xudmFyIExpbmtlZExpc3RfanNfMSA9IHJlcXVpcmUoXCIuLi91dGlsL0xpbmtlZExpc3QuanNcIik7XG52YXIgQWJzdHJhY3RNYXRoTGlzdCA9IGZ1bmN0aW9uIChfc3VwZXIpIHtcbiAgX19leHRlbmRzKEFic3RyYWN0TWF0aExpc3QsIF9zdXBlcik7XG4gIGZ1bmN0aW9uIEFic3RyYWN0TWF0aExpc3QoKSB7XG4gICAgcmV0dXJuIF9zdXBlciAhPT0gbnVsbCAmJiBfc3VwZXIuYXBwbHkodGhpcywgYXJndW1lbnRzKSB8fCB0aGlzO1xuICB9XG4gIEFic3RyYWN0TWF0aExpc3QucHJvdG90eXBlLmlzQmVmb3JlID0gZnVuY3Rpb24gKGEsIGIpIHtcbiAgICByZXR1cm4gYS5zdGFydC5pIDwgYi5zdGFydC5pIHx8IGEuc3RhcnQuaSA9PT0gYi5zdGFydC5pICYmIGEuc3RhcnQubiA8IGIuc3RhcnQubjtcbiAgfTtcbiAgcmV0dXJuIEFic3RyYWN0TWF0aExpc3Q7XG59KExpbmtlZExpc3RfanNfMS5MaW5rZWRMaXN0KTtcbmV4cG9ydHMuQWJzdHJhY3RNYXRoTGlzdCA9IEFic3RyYWN0TWF0aExpc3Q7IiwiXCJ1c2Ugc3RyaWN0XCI7XG5cbk9iamVjdC5kZWZpbmVQcm9wZXJ0eShleHBvcnRzLCBcIl9fZXNNb2R1bGVcIiwge1xuICB2YWx1ZTogdHJ1ZVxufSk7XG5leHBvcnRzLkFic3RyYWN0T3V0cHV0SmF4ID0gdm9pZCAwO1xudmFyIE9wdGlvbnNfanNfMSA9IHJlcXVpcmUoXCIuLi91dGlsL09wdGlvbnMuanNcIik7XG52YXIgRnVuY3Rpb25MaXN0X2pzXzEgPSByZXF1aXJlKFwiLi4vdXRpbC9GdW5jdGlvbkxpc3QuanNcIik7XG52YXIgQWJzdHJhY3RPdXRwdXRKYXggPSBmdW5jdGlvbiAoKSB7XG4gIGZ1bmN0aW9uIEFic3RyYWN0T3V0cHV0SmF4KG9wdGlvbnMpIHtcbiAgICBpZiAob3B0aW9ucyA9PT0gdm9pZCAwKSB7XG4gICAgICBvcHRpb25zID0ge307XG4gICAgfVxuICAgIHRoaXMuYWRhcHRvciA9IG51bGw7XG4gICAgdmFyIENMQVNTID0gdGhpcy5jb25zdHJ1Y3RvcjtcbiAgICB0aGlzLm9wdGlvbnMgPSAoMCwgT3B0aW9uc19qc18xLnVzZXJPcHRpb25zKSgoMCwgT3B0aW9uc19qc18xLmRlZmF1bHRPcHRpb25zKSh7fSwgQ0xBU1MuT1BUSU9OUyksIG9wdGlvbnMpO1xuICAgIHRoaXMucG9zdEZpbHRlcnMgPSBuZXcgRnVuY3Rpb25MaXN0X2pzXzEuRnVuY3Rpb25MaXN0KCk7XG4gIH1cbiAgT2JqZWN0LmRlZmluZVByb3BlcnR5KEFic3RyYWN0T3V0cHV0SmF4LnByb3RvdHlwZSwgXCJuYW1lXCIsIHtcbiAgICBnZXQ6IGZ1bmN0aW9uICgpIHtcbiAgICAgIHJldHVybiB0aGlzLmNvbnN0cnVjdG9yLk5BTUU7XG4gICAgfSxcbiAgICBlbnVtZXJhYmxlOiBmYWxzZSxcbiAgICBjb25maWd1cmFibGU6IHRydWVcbiAgfSk7XG4gIEFic3RyYWN0T3V0cHV0SmF4LnByb3RvdHlwZS5zZXRBZGFwdG9yID0gZnVuY3Rpb24gKGFkYXB0b3IpIHtcbiAgICB0aGlzLmFkYXB0b3IgPSBhZGFwdG9yO1xuICB9O1xuICBBYnN0cmFjdE91dHB1dEpheC5wcm90b3R5cGUuaW5pdGlhbGl6ZSA9IGZ1bmN0aW9uICgpIHt9O1xuICBBYnN0cmFjdE91dHB1dEpheC5wcm90b3R5cGUucmVzZXQgPSBmdW5jdGlvbiAoKSB7XG4gICAgdmFyIF9hcmdzID0gW107XG4gICAgZm9yICh2YXIgX2kgPSAwOyBfaSA8IGFyZ3VtZW50cy5sZW5ndGg7IF9pKyspIHtcbiAgICAgIF9hcmdzW19pXSA9IGFyZ3VtZW50c1tfaV07XG4gICAgfVxuICB9O1xuICBBYnN0cmFjdE91dHB1dEpheC5wcm90b3R5cGUuZ2V0TWV0cmljcyA9IGZ1bmN0aW9uIChfZG9jdW1lbnQpIHt9O1xuICBBYnN0cmFjdE91dHB1dEpheC5wcm90b3R5cGUuc3R5bGVTaGVldCA9IGZ1bmN0aW9uIChfZG9jdW1lbnQpIHtcbiAgICByZXR1cm4gbnVsbDtcbiAgfTtcbiAgQWJzdHJhY3RPdXRwdXRKYXgucHJvdG90eXBlLnBhZ2VFbGVtZW50cyA9IGZ1bmN0aW9uIChfZG9jdW1lbnQpIHtcbiAgICByZXR1cm4gbnVsbDtcbiAgfTtcbiAgQWJzdHJhY3RPdXRwdXRKYXgucHJvdG90eXBlLmV4ZWN1dGVGaWx0ZXJzID0gZnVuY3Rpb24gKGZpbHRlcnMsIG1hdGgsIGRvY3VtZW50LCBkYXRhKSB7XG4gICAgdmFyIGFyZ3MgPSB7XG4gICAgICBtYXRoOiBtYXRoLFxuICAgICAgZG9jdW1lbnQ6IGRvY3VtZW50LFxuICAgICAgZGF0YTogZGF0YVxuICAgIH07XG4gICAgZmlsdGVycy5leGVjdXRlKGFyZ3MpO1xuICAgIHJldHVybiBhcmdzLmRhdGE7XG4gIH07XG4gIEFic3RyYWN0T3V0cHV0SmF4Lk5BTUUgPSAnZ2VuZXJpYyc7XG4gIEFic3RyYWN0T3V0cHV0SmF4Lk9QVElPTlMgPSB7fTtcbiAgcmV0dXJuIEFic3RyYWN0T3V0cHV0SmF4O1xufSgpO1xuZXhwb3J0cy5BYnN0cmFjdE91dHB1dEpheCA9IEFic3RyYWN0T3V0cHV0SmF4OyIsIlwidXNlIHN0cmljdFwiO1xuXG52YXIgX19leHRlbmRzID0gdGhpcyAmJiB0aGlzLl9fZXh0ZW5kcyB8fCBmdW5jdGlvbiAoKSB7XG4gIHZhciBleHRlbmRTdGF0aWNzID0gZnVuY3Rpb24gKGQsIGIpIHtcbiAgICBleHRlbmRTdGF0aWNzID0gT2JqZWN0LnNldFByb3RvdHlwZU9mIHx8IHtcbiAgICAgIF9fcHJvdG9fXzogW11cbiAgICB9IGluc3RhbmNlb2YgQXJyYXkgJiYgZnVuY3Rpb24gKGQsIGIpIHtcbiAgICAgIGQuX19wcm90b19fID0gYjtcbiAgICB9IHx8IGZ1bmN0aW9uIChkLCBiKSB7XG4gICAgICBmb3IgKHZhciBwIGluIGIpIGlmIChPYmplY3QucHJvdG90eXBlLmhhc093blByb3BlcnR5LmNhbGwoYiwgcCkpIGRbcF0gPSBiW3BdO1xuICAgIH07XG4gICAgcmV0dXJuIGV4dGVuZFN0YXRpY3MoZCwgYik7XG4gIH07XG4gIHJldHVybiBmdW5jdGlvbiAoZCwgYikge1xuICAgIGlmICh0eXBlb2YgYiAhPT0gXCJmdW5jdGlvblwiICYmIGIgIT09IG51bGwpIHRocm93IG5ldyBUeXBlRXJyb3IoXCJDbGFzcyBleHRlbmRzIHZhbHVlIFwiICsgU3RyaW5nKGIpICsgXCIgaXMgbm90IGEgY29uc3RydWN0b3Igb3IgbnVsbFwiKTtcbiAgICBleHRlbmRTdGF0aWNzKGQsIGIpO1xuICAgIGZ1bmN0aW9uIF9fKCkge1xuICAgICAgdGhpcy5jb25zdHJ1Y3RvciA9IGQ7XG4gICAgfVxuICAgIGQucHJvdG90eXBlID0gYiA9PT0gbnVsbCA/IE9iamVjdC5jcmVhdGUoYikgOiAoX18ucHJvdG90eXBlID0gYi5wcm90b3R5cGUsIG5ldyBfXygpKTtcbiAgfTtcbn0oKTtcbnZhciBfX2Fzc2lnbiA9IHRoaXMgJiYgdGhpcy5fX2Fzc2lnbiB8fCBmdW5jdGlvbiAoKSB7XG4gIF9fYXNzaWduID0gT2JqZWN0LmFzc2lnbiB8fCBmdW5jdGlvbiAodCkge1xuICAgIGZvciAodmFyIHMsIGkgPSAxLCBuID0gYXJndW1lbnRzLmxlbmd0aDsgaSA8IG47IGkrKykge1xuICAgICAgcyA9IGFyZ3VtZW50c1tpXTtcbiAgICAgIGZvciAodmFyIHAgaW4gcykgaWYgKE9iamVjdC5wcm90b3R5cGUuaGFzT3duUHJvcGVydHkuY2FsbChzLCBwKSkgdFtwXSA9IHNbcF07XG4gICAgfVxuICAgIHJldHVybiB0O1xuICB9O1xuICByZXR1cm4gX19hc3NpZ24uYXBwbHkodGhpcywgYXJndW1lbnRzKTtcbn07XG52YXIgX19yZWFkID0gdGhpcyAmJiB0aGlzLl9fcmVhZCB8fCBmdW5jdGlvbiAobywgbikge1xuICB2YXIgbSA9IHR5cGVvZiBTeW1ib2wgPT09IFwiZnVuY3Rpb25cIiAmJiBvW1N5bWJvbC5pdGVyYXRvcl07XG4gIGlmICghbSkgcmV0dXJuIG87XG4gIHZhciBpID0gbS5jYWxsKG8pLFxuICAgIHIsXG4gICAgYXIgPSBbXSxcbiAgICBlO1xuICB0cnkge1xuICAgIHdoaWxlICgobiA9PT0gdm9pZCAwIHx8IG4tLSA+IDApICYmICEociA9IGkubmV4dCgpKS5kb25lKSBhci5wdXNoKHIudmFsdWUpO1xuICB9IGNhdGNoIChlcnJvcikge1xuICAgIGUgPSB7XG4gICAgICBlcnJvcjogZXJyb3JcbiAgICB9O1xuICB9IGZpbmFsbHkge1xuICAgIHRyeSB7XG4gICAgICBpZiAociAmJiAhci5kb25lICYmIChtID0gaVtcInJldHVyblwiXSkpIG0uY2FsbChpKTtcbiAgICB9IGZpbmFsbHkge1xuICAgICAgaWYgKGUpIHRocm93IGUuZXJyb3I7XG4gICAgfVxuICB9XG4gIHJldHVybiBhcjtcbn07XG52YXIgX192YWx1ZXMgPSB0aGlzICYmIHRoaXMuX192YWx1ZXMgfHwgZnVuY3Rpb24gKG8pIHtcbiAgdmFyIHMgPSB0eXBlb2YgU3ltYm9sID09PSBcImZ1bmN0aW9uXCIgJiYgU3ltYm9sLml0ZXJhdG9yLFxuICAgIG0gPSBzICYmIG9bc10sXG4gICAgaSA9IDA7XG4gIGlmIChtKSByZXR1cm4gbS5jYWxsKG8pO1xuICBpZiAobyAmJiB0eXBlb2Ygby5sZW5ndGggPT09IFwibnVtYmVyXCIpIHJldHVybiB7XG4gICAgbmV4dDogZnVuY3Rpb24gKCkge1xuICAgICAgaWYgKG8gJiYgaSA+PSBvLmxlbmd0aCkgbyA9IHZvaWQgMDtcbiAgICAgIHJldHVybiB7XG4gICAgICAgIHZhbHVlOiBvICYmIG9baSsrXSxcbiAgICAgICAgZG9uZTogIW9cbiAgICAgIH07XG4gICAgfVxuICB9O1xuICB0aHJvdyBuZXcgVHlwZUVycm9yKHMgPyBcIk9iamVjdCBpcyBub3QgaXRlcmFibGUuXCIgOiBcIlN5bWJvbC5pdGVyYXRvciBpcyBub3QgZGVmaW5lZC5cIik7XG59O1xuT2JqZWN0LmRlZmluZVByb3BlcnR5KGV4cG9ydHMsIFwiX19lc01vZHVsZVwiLCB7XG4gIHZhbHVlOiB0cnVlXG59KTtcbmV4cG9ydHMuSFRNTERvY3VtZW50ID0gdm9pZCAwO1xudmFyIE1hdGhEb2N1bWVudF9qc18xID0gcmVxdWlyZShcIi4uLy4uL2NvcmUvTWF0aERvY3VtZW50LmpzXCIpO1xudmFyIE9wdGlvbnNfanNfMSA9IHJlcXVpcmUoXCIuLi8uLi91dGlsL09wdGlvbnMuanNcIik7XG52YXIgSFRNTE1hdGhJdGVtX2pzXzEgPSByZXF1aXJlKFwiLi9IVE1MTWF0aEl0ZW0uanNcIik7XG52YXIgSFRNTE1hdGhMaXN0X2pzXzEgPSByZXF1aXJlKFwiLi9IVE1MTWF0aExpc3QuanNcIik7XG52YXIgSFRNTERvbVN0cmluZ3NfanNfMSA9IHJlcXVpcmUoXCIuL0hUTUxEb21TdHJpbmdzLmpzXCIpO1xudmFyIE1hdGhJdGVtX2pzXzEgPSByZXF1aXJlKFwiLi4vLi4vY29yZS9NYXRoSXRlbS5qc1wiKTtcbnZhciBIVE1MRG9jdW1lbnQgPSBmdW5jdGlvbiAoX3N1cGVyKSB7XG4gIF9fZXh0ZW5kcyhIVE1MRG9jdW1lbnQsIF9zdXBlcik7XG4gIGZ1bmN0aW9uIEhUTUxEb2N1bWVudChkb2N1bWVudCwgYWRhcHRvciwgb3B0aW9ucykge1xuICAgIHZhciBfdGhpcyA9IHRoaXM7XG4gICAgdmFyIF9hID0gX19yZWFkKCgwLCBPcHRpb25zX2pzXzEuc2VwYXJhdGVPcHRpb25zKShvcHRpb25zLCBIVE1MRG9tU3RyaW5nc19qc18xLkhUTUxEb21TdHJpbmdzLk9QVElPTlMpLCAyKSxcbiAgICAgIGh0bWwgPSBfYVswXSxcbiAgICAgIGRvbSA9IF9hWzFdO1xuICAgIF90aGlzID0gX3N1cGVyLmNhbGwodGhpcywgZG9jdW1lbnQsIGFkYXB0b3IsIGh0bWwpIHx8IHRoaXM7XG4gICAgX3RoaXMuZG9tU3RyaW5ncyA9IF90aGlzLm9wdGlvbnNbJ0RvbVN0cmluZ3MnXSB8fCBuZXcgSFRNTERvbVN0cmluZ3NfanNfMS5IVE1MRG9tU3RyaW5ncyhkb20pO1xuICAgIF90aGlzLmRvbVN0cmluZ3MuYWRhcHRvciA9IGFkYXB0b3I7XG4gICAgX3RoaXMuc3R5bGVzID0gW107XG4gICAgcmV0dXJuIF90aGlzO1xuICB9XG4gIEhUTUxEb2N1bWVudC5wcm90b3R5cGUuZmluZFBvc2l0aW9uID0gZnVuY3Rpb24gKE4sIGluZGV4LCBkZWxpbSwgbm9kZXMpIHtcbiAgICB2YXIgZV8xLCBfYTtcbiAgICB2YXIgYWRhcHRvciA9IHRoaXMuYWRhcHRvcjtcbiAgICB0cnkge1xuICAgICAgZm9yICh2YXIgX2IgPSBfX3ZhbHVlcyhub2Rlc1tOXSksIF9jID0gX2IubmV4dCgpOyAhX2MuZG9uZTsgX2MgPSBfYi5uZXh0KCkpIHtcbiAgICAgICAgdmFyIGxpc3QgPSBfYy52YWx1ZTtcbiAgICAgICAgdmFyIF9kID0gX19yZWFkKGxpc3QsIDIpLFxuICAgICAgICAgIG5vZGUgPSBfZFswXSxcbiAgICAgICAgICBuID0gX2RbMV07XG4gICAgICAgIGlmIChpbmRleCA8PSBuICYmIGFkYXB0b3Iua2luZChub2RlKSA9PT0gJyN0ZXh0Jykge1xuICAgICAgICAgIHJldHVybiB7XG4gICAgICAgICAgICBub2RlOiBub2RlLFxuICAgICAgICAgICAgbjogTWF0aC5tYXgoaW5kZXgsIDApLFxuICAgICAgICAgICAgZGVsaW06IGRlbGltXG4gICAgICAgICAgfTtcbiAgICAgICAgfVxuICAgICAgICBpbmRleCAtPSBuO1xuICAgICAgfVxuICAgIH0gY2F0Y2ggKGVfMV8xKSB7XG4gICAgICBlXzEgPSB7XG4gICAgICAgIGVycm9yOiBlXzFfMVxuICAgICAgfTtcbiAgICB9IGZpbmFsbHkge1xuICAgICAgdHJ5IHtcbiAgICAgICAgaWYgKF9jICYmICFfYy5kb25lICYmIChfYSA9IF9iLnJldHVybikpIF9hLmNhbGwoX2IpO1xuICAgICAgfSBmaW5hbGx5IHtcbiAgICAgICAgaWYgKGVfMSkgdGhyb3cgZV8xLmVycm9yO1xuICAgICAgfVxuICAgIH1cbiAgICByZXR1cm4ge1xuICAgICAgbm9kZTogbnVsbCxcbiAgICAgIG46IDAsXG4gICAgICBkZWxpbTogZGVsaW1cbiAgICB9O1xuICB9O1xuICBIVE1MRG9jdW1lbnQucHJvdG90eXBlLm1hdGhJdGVtID0gZnVuY3Rpb24gKGl0ZW0sIGpheCwgbm9kZXMpIHtcbiAgICB2YXIgbWF0aCA9IGl0ZW0ubWF0aDtcbiAgICB2YXIgc3RhcnQgPSB0aGlzLmZpbmRQb3NpdGlvbihpdGVtLm4sIGl0ZW0uc3RhcnQubiwgaXRlbS5vcGVuLCBub2Rlcyk7XG4gICAgdmFyIGVuZCA9IHRoaXMuZmluZFBvc2l0aW9uKGl0ZW0ubiwgaXRlbS5lbmQubiwgaXRlbS5jbG9zZSwgbm9kZXMpO1xuICAgIHJldHVybiBuZXcgdGhpcy5vcHRpb25zLk1hdGhJdGVtKG1hdGgsIGpheCwgaXRlbS5kaXNwbGF5LCBzdGFydCwgZW5kKTtcbiAgfTtcbiAgSFRNTERvY3VtZW50LnByb3RvdHlwZS5maW5kTWF0aCA9IGZ1bmN0aW9uIChvcHRpb25zKSB7XG4gICAgdmFyIGVfMiwgX2EsIGVfMywgX2IsIF9jLCBlXzQsIF9kLCBlXzUsIF9lO1xuICAgIGlmICghdGhpcy5wcm9jZXNzZWQuaXNTZXQoJ2ZpbmRNYXRoJykpIHtcbiAgICAgIHRoaXMuYWRhcHRvci5kb2N1bWVudCA9IHRoaXMuZG9jdW1lbnQ7XG4gICAgICBvcHRpb25zID0gKDAsIE9wdGlvbnNfanNfMS51c2VyT3B0aW9ucykoe1xuICAgICAgICBlbGVtZW50czogdGhpcy5vcHRpb25zLmVsZW1lbnRzIHx8IFt0aGlzLmFkYXB0b3IuYm9keSh0aGlzLmRvY3VtZW50KV1cbiAgICAgIH0sIG9wdGlvbnMpO1xuICAgICAgdHJ5IHtcbiAgICAgICAgZm9yICh2YXIgX2YgPSBfX3ZhbHVlcyh0aGlzLmFkYXB0b3IuZ2V0RWxlbWVudHMob3B0aW9uc1snZWxlbWVudHMnXSwgdGhpcy5kb2N1bWVudCkpLCBfZyA9IF9mLm5leHQoKTsgIV9nLmRvbmU7IF9nID0gX2YubmV4dCgpKSB7XG4gICAgICAgICAgdmFyIGNvbnRhaW5lciA9IF9nLnZhbHVlO1xuICAgICAgICAgIHZhciBfaCA9IF9fcmVhZChbbnVsbCwgbnVsbF0sIDIpLFxuICAgICAgICAgICAgc3RyaW5ncyA9IF9oWzBdLFxuICAgICAgICAgICAgbm9kZXMgPSBfaFsxXTtcbiAgICAgICAgICB0cnkge1xuICAgICAgICAgICAgZm9yICh2YXIgX2ogPSAoZV8zID0gdm9pZCAwLCBfX3ZhbHVlcyh0aGlzLmlucHV0SmF4KSksIF9rID0gX2oubmV4dCgpOyAhX2suZG9uZTsgX2sgPSBfai5uZXh0KCkpIHtcbiAgICAgICAgICAgICAgdmFyIGpheCA9IF9rLnZhbHVlO1xuICAgICAgICAgICAgICB2YXIgbGlzdCA9IG5ldyB0aGlzLm9wdGlvbnNbJ01hdGhMaXN0J10oKTtcbiAgICAgICAgICAgICAgaWYgKGpheC5wcm9jZXNzU3RyaW5ncykge1xuICAgICAgICAgICAgICAgIGlmIChzdHJpbmdzID09PSBudWxsKSB7XG4gICAgICAgICAgICAgICAgICBfYyA9IF9fcmVhZCh0aGlzLmRvbVN0cmluZ3MuZmluZChjb250YWluZXIpLCAyKSwgc3RyaW5ncyA9IF9jWzBdLCBub2RlcyA9IF9jWzFdO1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICB0cnkge1xuICAgICAgICAgICAgICAgICAgZm9yICh2YXIgX2wgPSAoZV80ID0gdm9pZCAwLCBfX3ZhbHVlcyhqYXguZmluZE1hdGgoc3RyaW5ncykpKSwgX20gPSBfbC5uZXh0KCk7ICFfbS5kb25lOyBfbSA9IF9sLm5leHQoKSkge1xuICAgICAgICAgICAgICAgICAgICB2YXIgbWF0aCA9IF9tLnZhbHVlO1xuICAgICAgICAgICAgICAgICAgICBsaXN0LnB1c2godGhpcy5tYXRoSXRlbShtYXRoLCBqYXgsIG5vZGVzKSk7XG4gICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgfSBjYXRjaCAoZV80XzEpIHtcbiAgICAgICAgICAgICAgICAgIGVfNCA9IHtcbiAgICAgICAgICAgICAgICAgICAgZXJyb3I6IGVfNF8xXG4gICAgICAgICAgICAgICAgICB9O1xuICAgICAgICAgICAgICAgIH0gZmluYWxseSB7XG4gICAgICAgICAgICAgICAgICB0cnkge1xuICAgICAgICAgICAgICAgICAgICBpZiAoX20gJiYgIV9tLmRvbmUgJiYgKF9kID0gX2wucmV0dXJuKSkgX2QuY2FsbChfbCk7XG4gICAgICAgICAgICAgICAgICB9IGZpbmFsbHkge1xuICAgICAgICAgICAgICAgICAgICBpZiAoZV80KSB0aHJvdyBlXzQuZXJyb3I7XG4gICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgICAgIHRyeSB7XG4gICAgICAgICAgICAgICAgICBmb3IgKHZhciBfbyA9IChlXzUgPSB2b2lkIDAsIF9fdmFsdWVzKGpheC5maW5kTWF0aChjb250YWluZXIpKSksIF9wID0gX28ubmV4dCgpOyAhX3AuZG9uZTsgX3AgPSBfby5uZXh0KCkpIHtcbiAgICAgICAgICAgICAgICAgICAgdmFyIG1hdGggPSBfcC52YWx1ZTtcbiAgICAgICAgICAgICAgICAgICAgdmFyIGl0ZW0gPSBuZXcgdGhpcy5vcHRpb25zLk1hdGhJdGVtKG1hdGgubWF0aCwgamF4LCBtYXRoLmRpc3BsYXksIG1hdGguc3RhcnQsIG1hdGguZW5kKTtcbiAgICAgICAgICAgICAgICAgICAgbGlzdC5wdXNoKGl0ZW0pO1xuICAgICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIH0gY2F0Y2ggKGVfNV8xKSB7XG4gICAgICAgICAgICAgICAgICBlXzUgPSB7XG4gICAgICAgICAgICAgICAgICAgIGVycm9yOiBlXzVfMVxuICAgICAgICAgICAgICAgICAgfTtcbiAgICAgICAgICAgICAgICB9IGZpbmFsbHkge1xuICAgICAgICAgICAgICAgICAgdHJ5IHtcbiAgICAgICAgICAgICAgICAgICAgaWYgKF9wICYmICFfcC5kb25lICYmIChfZSA9IF9vLnJldHVybikpIF9lLmNhbGwoX28pO1xuICAgICAgICAgICAgICAgICAgfSBmaW5hbGx5IHtcbiAgICAgICAgICAgICAgICAgICAgaWYgKGVfNSkgdGhyb3cgZV81LmVycm9yO1xuICAgICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICB0aGlzLm1hdGgubWVyZ2UobGlzdCk7XG4gICAgICAgICAgICB9XG4gICAgICAgICAgfSBjYXRjaCAoZV8zXzEpIHtcbiAgICAgICAgICAgIGVfMyA9IHtcbiAgICAgICAgICAgICAgZXJyb3I6IGVfM18xXG4gICAgICAgICAgICB9O1xuICAgICAgICAgIH0gZmluYWxseSB7XG4gICAgICAgICAgICB0cnkge1xuICAgICAgICAgICAgICBpZiAoX2sgJiYgIV9rLmRvbmUgJiYgKF9iID0gX2oucmV0dXJuKSkgX2IuY2FsbChfaik7XG4gICAgICAgICAgICB9IGZpbmFsbHkge1xuICAgICAgICAgICAgICBpZiAoZV8zKSB0aHJvdyBlXzMuZXJyb3I7XG4gICAgICAgICAgICB9XG4gICAgICAgICAgfVxuICAgICAgICB9XG4gICAgICB9IGNhdGNoIChlXzJfMSkge1xuICAgICAgICBlXzIgPSB7XG4gICAgICAgICAgZXJyb3I6IGVfMl8xXG4gICAgICAgIH07XG4gICAgICB9IGZpbmFsbHkge1xuICAgICAgICB0cnkge1xuICAgICAgICAgIGlmIChfZyAmJiAhX2cuZG9uZSAmJiAoX2EgPSBfZi5yZXR1cm4pKSBfYS5jYWxsKF9mKTtcbiAgICAgICAgfSBmaW5hbGx5IHtcbiAgICAgICAgICBpZiAoZV8yKSB0aHJvdyBlXzIuZXJyb3I7XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICAgIHRoaXMucHJvY2Vzc2VkLnNldCgnZmluZE1hdGgnKTtcbiAgICB9XG4gICAgcmV0dXJuIHRoaXM7XG4gIH07XG4gIEhUTUxEb2N1bWVudC5wcm90b3R5cGUudXBkYXRlRG9jdW1lbnQgPSBmdW5jdGlvbiAoKSB7XG4gICAgaWYgKCF0aGlzLnByb2Nlc3NlZC5pc1NldCgndXBkYXRlRG9jdW1lbnQnKSkge1xuICAgICAgdGhpcy5hZGRQYWdlRWxlbWVudHMoKTtcbiAgICAgIHRoaXMuYWRkU3R5bGVTaGVldCgpO1xuICAgICAgX3N1cGVyLnByb3RvdHlwZS51cGRhdGVEb2N1bWVudC5jYWxsKHRoaXMpO1xuICAgICAgdGhpcy5wcm9jZXNzZWQuc2V0KCd1cGRhdGVEb2N1bWVudCcpO1xuICAgIH1cbiAgICByZXR1cm4gdGhpcztcbiAgfTtcbiAgSFRNTERvY3VtZW50LnByb3RvdHlwZS5hZGRQYWdlRWxlbWVudHMgPSBmdW5jdGlvbiAoKSB7XG4gICAgdmFyIGJvZHkgPSB0aGlzLmFkYXB0b3IuYm9keSh0aGlzLmRvY3VtZW50KTtcbiAgICB2YXIgbm9kZSA9IHRoaXMuZG9jdW1lbnRQYWdlRWxlbWVudHMoKTtcbiAgICBpZiAobm9kZSkge1xuICAgICAgdGhpcy5hZGFwdG9yLmFwcGVuZChib2R5LCBub2RlKTtcbiAgICB9XG4gIH07XG4gIEhUTUxEb2N1bWVudC5wcm90b3R5cGUuYWRkU3R5bGVTaGVldCA9IGZ1bmN0aW9uICgpIHtcbiAgICB2YXIgc2hlZXQgPSB0aGlzLmRvY3VtZW50U3R5bGVTaGVldCgpO1xuICAgIHZhciBhZGFwdG9yID0gdGhpcy5hZGFwdG9yO1xuICAgIGlmIChzaGVldCAmJiAhYWRhcHRvci5wYXJlbnQoc2hlZXQpKSB7XG4gICAgICB2YXIgaGVhZCA9IGFkYXB0b3IuaGVhZCh0aGlzLmRvY3VtZW50KTtcbiAgICAgIHZhciBzdHlsZXMgPSB0aGlzLmZpbmRTaGVldChoZWFkLCBhZGFwdG9yLmdldEF0dHJpYnV0ZShzaGVldCwgJ2lkJykpO1xuICAgICAgaWYgKHN0eWxlcykge1xuICAgICAgICBhZGFwdG9yLnJlcGxhY2Uoc2hlZXQsIHN0eWxlcyk7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICBhZGFwdG9yLmFwcGVuZChoZWFkLCBzaGVldCk7XG4gICAgICB9XG4gICAgfVxuICB9O1xuICBIVE1MRG9jdW1lbnQucHJvdG90eXBlLmZpbmRTaGVldCA9IGZ1bmN0aW9uIChoZWFkLCBpZCkge1xuICAgIHZhciBlXzYsIF9hO1xuICAgIGlmIChpZCkge1xuICAgICAgdHJ5IHtcbiAgICAgICAgZm9yICh2YXIgX2IgPSBfX3ZhbHVlcyh0aGlzLmFkYXB0b3IudGFncyhoZWFkLCAnc3R5bGUnKSksIF9jID0gX2IubmV4dCgpOyAhX2MuZG9uZTsgX2MgPSBfYi5uZXh0KCkpIHtcbiAgICAgICAgICB2YXIgc2hlZXQgPSBfYy52YWx1ZTtcbiAgICAgICAgICBpZiAodGhpcy5hZGFwdG9yLmdldEF0dHJpYnV0ZShzaGVldCwgJ2lkJykgPT09IGlkKSB7XG4gICAgICAgICAgICByZXR1cm4gc2hlZXQ7XG4gICAgICAgICAgfVxuICAgICAgICB9XG4gICAgICB9IGNhdGNoIChlXzZfMSkge1xuICAgICAgICBlXzYgPSB7XG4gICAgICAgICAgZXJyb3I6IGVfNl8xXG4gICAgICAgIH07XG4gICAgICB9IGZpbmFsbHkge1xuICAgICAgICB0cnkge1xuICAgICAgICAgIGlmIChfYyAmJiAhX2MuZG9uZSAmJiAoX2EgPSBfYi5yZXR1cm4pKSBfYS5jYWxsKF9iKTtcbiAgICAgICAgfSBmaW5hbGx5IHtcbiAgICAgICAgICBpZiAoZV82KSB0aHJvdyBlXzYuZXJyb3I7XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9XG4gICAgcmV0dXJuIG51bGw7XG4gIH07XG4gIEhUTUxEb2N1bWVudC5wcm90b3R5cGUucmVtb3ZlRnJvbURvY3VtZW50ID0gZnVuY3Rpb24gKHJlc3RvcmUpIHtcbiAgICB2YXIgZV83LCBfYTtcbiAgICBpZiAocmVzdG9yZSA9PT0gdm9pZCAwKSB7XG4gICAgICByZXN0b3JlID0gZmFsc2U7XG4gICAgfVxuICAgIGlmICh0aGlzLnByb2Nlc3NlZC5pc1NldCgndXBkYXRlRG9jdW1lbnQnKSkge1xuICAgICAgdHJ5IHtcbiAgICAgICAgZm9yICh2YXIgX2IgPSBfX3ZhbHVlcyh0aGlzLm1hdGgpLCBfYyA9IF9iLm5leHQoKTsgIV9jLmRvbmU7IF9jID0gX2IubmV4dCgpKSB7XG4gICAgICAgICAgdmFyIG1hdGggPSBfYy52YWx1ZTtcbiAgICAgICAgICBpZiAobWF0aC5zdGF0ZSgpID49IE1hdGhJdGVtX2pzXzEuU1RBVEUuSU5TRVJURUQpIHtcbiAgICAgICAgICAgIG1hdGguc3RhdGUoTWF0aEl0ZW1fanNfMS5TVEFURS5UWVBFU0VULCByZXN0b3JlKTtcbiAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICAgIH0gY2F0Y2ggKGVfN18xKSB7XG4gICAgICAgIGVfNyA9IHtcbiAgICAgICAgICBlcnJvcjogZV83XzFcbiAgICAgICAgfTtcbiAgICAgIH0gZmluYWxseSB7XG4gICAgICAgIHRyeSB7XG4gICAgICAgICAgaWYgKF9jICYmICFfYy5kb25lICYmIChfYSA9IF9iLnJldHVybikpIF9hLmNhbGwoX2IpO1xuICAgICAgICB9IGZpbmFsbHkge1xuICAgICAgICAgIGlmIChlXzcpIHRocm93IGVfNy5lcnJvcjtcbiAgICAgICAgfVxuICAgICAgfVxuICAgIH1cbiAgICB0aGlzLnByb2Nlc3NlZC5jbGVhcigndXBkYXRlRG9jdW1lbnQnKTtcbiAgICByZXR1cm4gdGhpcztcbiAgfTtcbiAgSFRNTERvY3VtZW50LnByb3RvdHlwZS5kb2N1bWVudFN0eWxlU2hlZXQgPSBmdW5jdGlvbiAoKSB7XG4gICAgcmV0dXJuIHRoaXMub3V0cHV0SmF4LnN0eWxlU2hlZXQodGhpcyk7XG4gIH07XG4gIEhUTUxEb2N1bWVudC5wcm90b3R5cGUuZG9jdW1lbnRQYWdlRWxlbWVudHMgPSBmdW5jdGlvbiAoKSB7XG4gICAgcmV0dXJuIHRoaXMub3V0cHV0SmF4LnBhZ2VFbGVtZW50cyh0aGlzKTtcbiAgfTtcbiAgSFRNTERvY3VtZW50LnByb3RvdHlwZS5hZGRTdHlsZXMgPSBmdW5jdGlvbiAoc3R5bGVzKSB7XG4gICAgdGhpcy5zdHlsZXMucHVzaChzdHlsZXMpO1xuICB9O1xuICBIVE1MRG9jdW1lbnQucHJvdG90eXBlLmdldFN0eWxlcyA9IGZ1bmN0aW9uICgpIHtcbiAgICByZXR1cm4gdGhpcy5zdHlsZXM7XG4gIH07XG4gIEhUTUxEb2N1bWVudC5LSU5EID0gJ0hUTUwnO1xuICBIVE1MRG9jdW1lbnQuT1BUSU9OUyA9IF9fYXNzaWduKF9fYXNzaWduKHt9LCBNYXRoRG9jdW1lbnRfanNfMS5BYnN0cmFjdE1hdGhEb2N1bWVudC5PUFRJT05TKSwge1xuICAgIHJlbmRlckFjdGlvbnM6ICgwLCBPcHRpb25zX2pzXzEuZXhwYW5kYWJsZSkoX19hc3NpZ24oX19hc3NpZ24oe30sIE1hdGhEb2N1bWVudF9qc18xLkFic3RyYWN0TWF0aERvY3VtZW50Lk9QVElPTlMucmVuZGVyQWN0aW9ucyksIHtcbiAgICAgIHN0eWxlczogW01hdGhJdGVtX2pzXzEuU1RBVEUuSU5TRVJURUQgKyAxLCAnJywgJ3VwZGF0ZVN0eWxlU2hlZXQnLCBmYWxzZV1cbiAgICB9KSksXG4gICAgTWF0aExpc3Q6IEhUTUxNYXRoTGlzdF9qc18xLkhUTUxNYXRoTGlzdCxcbiAgICBNYXRoSXRlbTogSFRNTE1hdGhJdGVtX2pzXzEuSFRNTE1hdGhJdGVtLFxuICAgIERvbVN0cmluZ3M6IG51bGxcbiAgfSk7XG4gIHJldHVybiBIVE1MRG9jdW1lbnQ7XG59KE1hdGhEb2N1bWVudF9qc18xLkFic3RyYWN0TWF0aERvY3VtZW50KTtcbmV4cG9ydHMuSFRNTERvY3VtZW50ID0gSFRNTERvY3VtZW50OyIsIlwidXNlIHN0cmljdFwiO1xuXG52YXIgX19yZWFkID0gdGhpcyAmJiB0aGlzLl9fcmVhZCB8fCBmdW5jdGlvbiAobywgbikge1xuICB2YXIgbSA9IHR5cGVvZiBTeW1ib2wgPT09IFwiZnVuY3Rpb25cIiAmJiBvW1N5bWJvbC5pdGVyYXRvcl07XG4gIGlmICghbSkgcmV0dXJuIG87XG4gIHZhciBpID0gbS5jYWxsKG8pLFxuICAgIHIsXG4gICAgYXIgPSBbXSxcbiAgICBlO1xuICB0cnkge1xuICAgIHdoaWxlICgobiA9PT0gdm9pZCAwIHx8IG4tLSA+IDApICYmICEociA9IGkubmV4dCgpKS5kb25lKSBhci5wdXNoKHIudmFsdWUpO1xuICB9IGNhdGNoIChlcnJvcikge1xuICAgIGUgPSB7XG4gICAgICBlcnJvcjogZXJyb3JcbiAgICB9O1xuICB9IGZpbmFsbHkge1xuICAgIHRyeSB7XG4gICAgICBpZiAociAmJiAhci5kb25lICYmIChtID0gaVtcInJldHVyblwiXSkpIG0uY2FsbChpKTtcbiAgICB9IGZpbmFsbHkge1xuICAgICAgaWYgKGUpIHRocm93IGUuZXJyb3I7XG4gICAgfVxuICB9XG4gIHJldHVybiBhcjtcbn07XG5PYmplY3QuZGVmaW5lUHJvcGVydHkoZXhwb3J0cywgXCJfX2VzTW9kdWxlXCIsIHtcbiAgdmFsdWU6IHRydWVcbn0pO1xuZXhwb3J0cy5IVE1MRG9tU3RyaW5ncyA9IHZvaWQgMDtcbnZhciBPcHRpb25zX2pzXzEgPSByZXF1aXJlKFwiLi4vLi4vdXRpbC9PcHRpb25zLmpzXCIpO1xudmFyIEhUTUxEb21TdHJpbmdzID0gZnVuY3Rpb24gKCkge1xuICBmdW5jdGlvbiBIVE1MRG9tU3RyaW5ncyhvcHRpb25zKSB7XG4gICAgaWYgKG9wdGlvbnMgPT09IHZvaWQgMCkge1xuICAgICAgb3B0aW9ucyA9IG51bGw7XG4gICAgfVxuICAgIHZhciBDTEFTUyA9IHRoaXMuY29uc3RydWN0b3I7XG4gICAgdGhpcy5vcHRpb25zID0gKDAsIE9wdGlvbnNfanNfMS51c2VyT3B0aW9ucykoKDAsIE9wdGlvbnNfanNfMS5kZWZhdWx0T3B0aW9ucykoe30sIENMQVNTLk9QVElPTlMpLCBvcHRpb25zKTtcbiAgICB0aGlzLmluaXQoKTtcbiAgICB0aGlzLmdldFBhdHRlcm5zKCk7XG4gIH1cbiAgSFRNTERvbVN0cmluZ3MucHJvdG90eXBlLmluaXQgPSBmdW5jdGlvbiAoKSB7XG4gICAgdGhpcy5zdHJpbmdzID0gW107XG4gICAgdGhpcy5zdHJpbmcgPSAnJztcbiAgICB0aGlzLnNub2RlcyA9IFtdO1xuICAgIHRoaXMubm9kZXMgPSBbXTtcbiAgICB0aGlzLnN0YWNrID0gW107XG4gIH07XG4gIEhUTUxEb21TdHJpbmdzLnByb3RvdHlwZS5nZXRQYXR0ZXJucyA9IGZ1bmN0aW9uICgpIHtcbiAgICB2YXIgc2tpcCA9ICgwLCBPcHRpb25zX2pzXzEubWFrZUFycmF5KSh0aGlzLm9wdGlvbnNbJ3NraXBIdG1sVGFncyddKTtcbiAgICB2YXIgaWdub3JlID0gKDAsIE9wdGlvbnNfanNfMS5tYWtlQXJyYXkpKHRoaXMub3B0aW9uc1snaWdub3JlSHRtbENsYXNzJ10pO1xuICAgIHZhciBwcm9jZXNzID0gKDAsIE9wdGlvbnNfanNfMS5tYWtlQXJyYXkpKHRoaXMub3B0aW9uc1sncHJvY2Vzc0h0bWxDbGFzcyddKTtcbiAgICB0aGlzLnNraXBIdG1sVGFncyA9IG5ldyBSZWdFeHAoJ14oPzonICsgc2tpcC5qb2luKCd8JykgKyAnKSQnLCAnaScpO1xuICAgIHRoaXMuaWdub3JlSHRtbENsYXNzID0gbmV3IFJlZ0V4cCgnKD86XnwgKSg/OicgKyBpZ25vcmUuam9pbignfCcpICsgJykoPzogfCQpJyk7XG4gICAgdGhpcy5wcm9jZXNzSHRtbENsYXNzID0gbmV3IFJlZ0V4cCgnKD86XnwgKSg/OicgKyBwcm9jZXNzICsgJykoPzogfCQpJyk7XG4gIH07XG4gIEhUTUxEb21TdHJpbmdzLnByb3RvdHlwZS5wdXNoU3RyaW5nID0gZnVuY3Rpb24gKCkge1xuICAgIGlmICh0aGlzLnN0cmluZy5tYXRjaCgvXFxTLykpIHtcbiAgICAgIHRoaXMuc3RyaW5ncy5wdXNoKHRoaXMuc3RyaW5nKTtcbiAgICAgIHRoaXMubm9kZXMucHVzaCh0aGlzLnNub2Rlcyk7XG4gICAgfVxuICAgIHRoaXMuc3RyaW5nID0gJyc7XG4gICAgdGhpcy5zbm9kZXMgPSBbXTtcbiAgfTtcbiAgSFRNTERvbVN0cmluZ3MucHJvdG90eXBlLmV4dGVuZFN0cmluZyA9IGZ1bmN0aW9uIChub2RlLCB0ZXh0KSB7XG4gICAgdGhpcy5zbm9kZXMucHVzaChbbm9kZSwgdGV4dC5sZW5ndGhdKTtcbiAgICB0aGlzLnN0cmluZyArPSB0ZXh0O1xuICB9O1xuICBIVE1MRG9tU3RyaW5ncy5wcm90b3R5cGUuaGFuZGxlVGV4dCA9IGZ1bmN0aW9uIChub2RlLCBpZ25vcmUpIHtcbiAgICBpZiAoIWlnbm9yZSkge1xuICAgICAgdGhpcy5leHRlbmRTdHJpbmcobm9kZSwgdGhpcy5hZGFwdG9yLnZhbHVlKG5vZGUpKTtcbiAgICB9XG4gICAgcmV0dXJuIHRoaXMuYWRhcHRvci5uZXh0KG5vZGUpO1xuICB9O1xuICBIVE1MRG9tU3RyaW5ncy5wcm90b3R5cGUuaGFuZGxlVGFnID0gZnVuY3Rpb24gKG5vZGUsIGlnbm9yZSkge1xuICAgIGlmICghaWdub3JlKSB7XG4gICAgICB2YXIgdGV4dCA9IHRoaXMub3B0aW9uc1snaW5jbHVkZUh0bWxUYWdzJ11bdGhpcy5hZGFwdG9yLmtpbmQobm9kZSldO1xuICAgICAgdGhpcy5leHRlbmRTdHJpbmcobm9kZSwgdGV4dCk7XG4gICAgfVxuICAgIHJldHVybiB0aGlzLmFkYXB0b3IubmV4dChub2RlKTtcbiAgfTtcbiAgSFRNTERvbVN0cmluZ3MucHJvdG90eXBlLmhhbmRsZUNvbnRhaW5lciA9IGZ1bmN0aW9uIChub2RlLCBpZ25vcmUpIHtcbiAgICB0aGlzLnB1c2hTdHJpbmcoKTtcbiAgICB2YXIgY25hbWUgPSB0aGlzLmFkYXB0b3IuZ2V0QXR0cmlidXRlKG5vZGUsICdjbGFzcycpIHx8ICcnO1xuICAgIHZhciB0bmFtZSA9IHRoaXMuYWRhcHRvci5raW5kKG5vZGUpIHx8ICcnO1xuICAgIHZhciBwcm9jZXNzID0gdGhpcy5wcm9jZXNzSHRtbENsYXNzLmV4ZWMoY25hbWUpO1xuICAgIHZhciBuZXh0ID0gbm9kZTtcbiAgICBpZiAodGhpcy5hZGFwdG9yLmZpcnN0Q2hpbGQobm9kZSkgJiYgIXRoaXMuYWRhcHRvci5nZXRBdHRyaWJ1dGUobm9kZSwgJ2RhdGEtTUpYJykgJiYgKHByb2Nlc3MgfHwgIXRoaXMuc2tpcEh0bWxUYWdzLmV4ZWModG5hbWUpKSkge1xuICAgICAgaWYgKHRoaXMuYWRhcHRvci5uZXh0KG5vZGUpKSB7XG4gICAgICAgIHRoaXMuc3RhY2sucHVzaChbdGhpcy5hZGFwdG9yLm5leHQobm9kZSksIGlnbm9yZV0pO1xuICAgICAgfVxuICAgICAgbmV4dCA9IHRoaXMuYWRhcHRvci5maXJzdENoaWxkKG5vZGUpO1xuICAgICAgaWdub3JlID0gKGlnbm9yZSB8fCB0aGlzLmlnbm9yZUh0bWxDbGFzcy5leGVjKGNuYW1lKSkgJiYgIXByb2Nlc3M7XG4gICAgfSBlbHNlIHtcbiAgICAgIG5leHQgPSB0aGlzLmFkYXB0b3IubmV4dChub2RlKTtcbiAgICB9XG4gICAgcmV0dXJuIFtuZXh0LCBpZ25vcmVdO1xuICB9O1xuICBIVE1MRG9tU3RyaW5ncy5wcm90b3R5cGUuaGFuZGxlT3RoZXIgPSBmdW5jdGlvbiAobm9kZSwgX2lnbm9yZSkge1xuICAgIHRoaXMucHVzaFN0cmluZygpO1xuICAgIHJldHVybiB0aGlzLmFkYXB0b3IubmV4dChub2RlKTtcbiAgfTtcbiAgSFRNTERvbVN0cmluZ3MucHJvdG90eXBlLmZpbmQgPSBmdW5jdGlvbiAobm9kZSkge1xuICAgIHZhciBfYSwgX2I7XG4gICAgdGhpcy5pbml0KCk7XG4gICAgdmFyIHN0b3AgPSB0aGlzLmFkYXB0b3IubmV4dChub2RlKTtcbiAgICB2YXIgaWdub3JlID0gZmFsc2U7XG4gICAgdmFyIGluY2x1ZGUgPSB0aGlzLm9wdGlvbnNbJ2luY2x1ZGVIdG1sVGFncyddO1xuICAgIHdoaWxlIChub2RlICYmIG5vZGUgIT09IHN0b3ApIHtcbiAgICAgIHZhciBraW5kID0gdGhpcy5hZGFwdG9yLmtpbmQobm9kZSk7XG4gICAgICBpZiAoa2luZCA9PT0gJyN0ZXh0Jykge1xuICAgICAgICBub2RlID0gdGhpcy5oYW5kbGVUZXh0KG5vZGUsIGlnbm9yZSk7XG4gICAgICB9IGVsc2UgaWYgKGluY2x1ZGUuaGFzT3duUHJvcGVydHkoa2luZCkpIHtcbiAgICAgICAgbm9kZSA9IHRoaXMuaGFuZGxlVGFnKG5vZGUsIGlnbm9yZSk7XG4gICAgICB9IGVsc2UgaWYgKGtpbmQpIHtcbiAgICAgICAgX2EgPSBfX3JlYWQodGhpcy5oYW5kbGVDb250YWluZXIobm9kZSwgaWdub3JlKSwgMiksIG5vZGUgPSBfYVswXSwgaWdub3JlID0gX2FbMV07XG4gICAgICB9IGVsc2Uge1xuICAgICAgICBub2RlID0gdGhpcy5oYW5kbGVPdGhlcihub2RlLCBpZ25vcmUpO1xuICAgICAgfVxuICAgICAgaWYgKCFub2RlICYmIHRoaXMuc3RhY2subGVuZ3RoKSB7XG4gICAgICAgIHRoaXMucHVzaFN0cmluZygpO1xuICAgICAgICBfYiA9IF9fcmVhZCh0aGlzLnN0YWNrLnBvcCgpLCAyKSwgbm9kZSA9IF9iWzBdLCBpZ25vcmUgPSBfYlsxXTtcbiAgICAgIH1cbiAgICB9XG4gICAgdGhpcy5wdXNoU3RyaW5nKCk7XG4gICAgdmFyIHJlc3VsdCA9IFt0aGlzLnN0cmluZ3MsIHRoaXMubm9kZXNdO1xuICAgIHRoaXMuaW5pdCgpO1xuICAgIHJldHVybiByZXN1bHQ7XG4gIH07XG4gIEhUTUxEb21TdHJpbmdzLk9QVElPTlMgPSB7XG4gICAgc2tpcEh0bWxUYWdzOiBbJ3NjcmlwdCcsICdub3NjcmlwdCcsICdzdHlsZScsICd0ZXh0YXJlYScsICdwcmUnLCAnY29kZScsICdhbm5vdGF0aW9uJywgJ2Fubm90YXRpb24teG1sJ10sXG4gICAgaW5jbHVkZUh0bWxUYWdzOiB7XG4gICAgICBicjogJ1xcbicsXG4gICAgICB3YnI6ICcnLFxuICAgICAgJyNjb21tZW50JzogJydcbiAgICB9LFxuICAgIGlnbm9yZUh0bWxDbGFzczogJ21hdGhqYXhfaWdub3JlJyxcbiAgICBwcm9jZXNzSHRtbENsYXNzOiAnbWF0aGpheF9wcm9jZXNzJ1xuICB9O1xuICByZXR1cm4gSFRNTERvbVN0cmluZ3M7XG59KCk7XG5leHBvcnRzLkhUTUxEb21TdHJpbmdzID0gSFRNTERvbVN0cmluZ3M7IiwiXCJ1c2Ugc3RyaWN0XCI7XG5cbnZhciBfX2V4dGVuZHMgPSB0aGlzICYmIHRoaXMuX19leHRlbmRzIHx8IGZ1bmN0aW9uICgpIHtcbiAgdmFyIGV4dGVuZFN0YXRpY3MgPSBmdW5jdGlvbiAoZCwgYikge1xuICAgIGV4dGVuZFN0YXRpY3MgPSBPYmplY3Quc2V0UHJvdG90eXBlT2YgfHwge1xuICAgICAgX19wcm90b19fOiBbXVxuICAgIH0gaW5zdGFuY2VvZiBBcnJheSAmJiBmdW5jdGlvbiAoZCwgYikge1xuICAgICAgZC5fX3Byb3RvX18gPSBiO1xuICAgIH0gfHwgZnVuY3Rpb24gKGQsIGIpIHtcbiAgICAgIGZvciAodmFyIHAgaW4gYikgaWYgKE9iamVjdC5wcm90b3R5cGUuaGFzT3duUHJvcGVydHkuY2FsbChiLCBwKSkgZFtwXSA9IGJbcF07XG4gICAgfTtcbiAgICByZXR1cm4gZXh0ZW5kU3RhdGljcyhkLCBiKTtcbiAgfTtcbiAgcmV0dXJuIGZ1bmN0aW9uIChkLCBiKSB7XG4gICAgaWYgKHR5cGVvZiBiICE9PSBcImZ1bmN0aW9uXCIgJiYgYiAhPT0gbnVsbCkgdGhyb3cgbmV3IFR5cGVFcnJvcihcIkNsYXNzIGV4dGVuZHMgdmFsdWUgXCIgKyBTdHJpbmcoYikgKyBcIiBpcyBub3QgYSBjb25zdHJ1Y3RvciBvciBudWxsXCIpO1xuICAgIGV4dGVuZFN0YXRpY3MoZCwgYik7XG4gICAgZnVuY3Rpb24gX18oKSB7XG4gICAgICB0aGlzLmNvbnN0cnVjdG9yID0gZDtcbiAgICB9XG4gICAgZC5wcm90b3R5cGUgPSBiID09PSBudWxsID8gT2JqZWN0LmNyZWF0ZShiKSA6IChfXy5wcm90b3R5cGUgPSBiLnByb3RvdHlwZSwgbmV3IF9fKCkpO1xuICB9O1xufSgpO1xuT2JqZWN0LmRlZmluZVByb3BlcnR5KGV4cG9ydHMsIFwiX19lc01vZHVsZVwiLCB7XG4gIHZhbHVlOiB0cnVlXG59KTtcbmV4cG9ydHMuSFRNTEhhbmRsZXIgPSB2b2lkIDA7XG52YXIgSGFuZGxlcl9qc18xID0gcmVxdWlyZShcIi4uLy4uL2NvcmUvSGFuZGxlci5qc1wiKTtcbnZhciBIVE1MRG9jdW1lbnRfanNfMSA9IHJlcXVpcmUoXCIuL0hUTUxEb2N1bWVudC5qc1wiKTtcbnZhciBIVE1MSGFuZGxlciA9IGZ1bmN0aW9uIChfc3VwZXIpIHtcbiAgX19leHRlbmRzKEhUTUxIYW5kbGVyLCBfc3VwZXIpO1xuICBmdW5jdGlvbiBIVE1MSGFuZGxlcigpIHtcbiAgICB2YXIgX3RoaXMgPSBfc3VwZXIgIT09IG51bGwgJiYgX3N1cGVyLmFwcGx5KHRoaXMsIGFyZ3VtZW50cykgfHwgdGhpcztcbiAgICBfdGhpcy5kb2N1bWVudENsYXNzID0gSFRNTERvY3VtZW50X2pzXzEuSFRNTERvY3VtZW50O1xuICAgIHJldHVybiBfdGhpcztcbiAgfVxuICBIVE1MSGFuZGxlci5wcm90b3R5cGUuaGFuZGxlc0RvY3VtZW50ID0gZnVuY3Rpb24gKGRvY3VtZW50KSB7XG4gICAgdmFyIGFkYXB0b3IgPSB0aGlzLmFkYXB0b3I7XG4gICAgaWYgKHR5cGVvZiBkb2N1bWVudCA9PT0gJ3N0cmluZycpIHtcbiAgICAgIHRyeSB7XG4gICAgICAgIGRvY3VtZW50ID0gYWRhcHRvci5wYXJzZShkb2N1bWVudCwgJ3RleHQvaHRtbCcpO1xuICAgICAgfSBjYXRjaCAoZXJyKSB7fVxuICAgIH1cbiAgICBpZiAoZG9jdW1lbnQgaW5zdGFuY2VvZiBhZGFwdG9yLndpbmRvdy5Eb2N1bWVudCB8fCBkb2N1bWVudCBpbnN0YW5jZW9mIGFkYXB0b3Iud2luZG93LkhUTUxFbGVtZW50IHx8IGRvY3VtZW50IGluc3RhbmNlb2YgYWRhcHRvci53aW5kb3cuRG9jdW1lbnRGcmFnbWVudCkge1xuICAgICAgcmV0dXJuIHRydWU7XG4gICAgfVxuICAgIHJldHVybiBmYWxzZTtcbiAgfTtcbiAgSFRNTEhhbmRsZXIucHJvdG90eXBlLmNyZWF0ZSA9IGZ1bmN0aW9uIChkb2N1bWVudCwgb3B0aW9ucykge1xuICAgIHZhciBhZGFwdG9yID0gdGhpcy5hZGFwdG9yO1xuICAgIGlmICh0eXBlb2YgZG9jdW1lbnQgPT09ICdzdHJpbmcnKSB7XG4gICAgICBkb2N1bWVudCA9IGFkYXB0b3IucGFyc2UoZG9jdW1lbnQsICd0ZXh0L2h0bWwnKTtcbiAgICB9IGVsc2UgaWYgKGRvY3VtZW50IGluc3RhbmNlb2YgYWRhcHRvci53aW5kb3cuSFRNTEVsZW1lbnQgfHwgZG9jdW1lbnQgaW5zdGFuY2VvZiBhZGFwdG9yLndpbmRvdy5Eb2N1bWVudEZyYWdtZW50KSB7XG4gICAgICB2YXIgY2hpbGQgPSBkb2N1bWVudDtcbiAgICAgIGRvY3VtZW50ID0gYWRhcHRvci5wYXJzZSgnJywgJ3RleHQvaHRtbCcpO1xuICAgICAgYWRhcHRvci5hcHBlbmQoYWRhcHRvci5ib2R5KGRvY3VtZW50KSwgY2hpbGQpO1xuICAgIH1cbiAgICByZXR1cm4gX3N1cGVyLnByb3RvdHlwZS5jcmVhdGUuY2FsbCh0aGlzLCBkb2N1bWVudCwgb3B0aW9ucyk7XG4gIH07XG4gIHJldHVybiBIVE1MSGFuZGxlcjtcbn0oSGFuZGxlcl9qc18xLkFic3RyYWN0SGFuZGxlcik7XG5leHBvcnRzLkhUTUxIYW5kbGVyID0gSFRNTEhhbmRsZXI7IiwiXCJ1c2Ugc3RyaWN0XCI7XG5cbnZhciBfX2V4dGVuZHMgPSB0aGlzICYmIHRoaXMuX19leHRlbmRzIHx8IGZ1bmN0aW9uICgpIHtcbiAgdmFyIGV4dGVuZFN0YXRpY3MgPSBmdW5jdGlvbiAoZCwgYikge1xuICAgIGV4dGVuZFN0YXRpY3MgPSBPYmplY3Quc2V0UHJvdG90eXBlT2YgfHwge1xuICAgICAgX19wcm90b19fOiBbXVxuICAgIH0gaW5zdGFuY2VvZiBBcnJheSAmJiBmdW5jdGlvbiAoZCwgYikge1xuICAgICAgZC5fX3Byb3RvX18gPSBiO1xuICAgIH0gfHwgZnVuY3Rpb24gKGQsIGIpIHtcbiAgICAgIGZvciAodmFyIHAgaW4gYikgaWYgKE9iamVjdC5wcm90b3R5cGUuaGFzT3duUHJvcGVydHkuY2FsbChiLCBwKSkgZFtwXSA9IGJbcF07XG4gICAgfTtcbiAgICByZXR1cm4gZXh0ZW5kU3RhdGljcyhkLCBiKTtcbiAgfTtcbiAgcmV0dXJuIGZ1bmN0aW9uIChkLCBiKSB7XG4gICAgaWYgKHR5cGVvZiBiICE9PSBcImZ1bmN0aW9uXCIgJiYgYiAhPT0gbnVsbCkgdGhyb3cgbmV3IFR5cGVFcnJvcihcIkNsYXNzIGV4dGVuZHMgdmFsdWUgXCIgKyBTdHJpbmcoYikgKyBcIiBpcyBub3QgYSBjb25zdHJ1Y3RvciBvciBudWxsXCIpO1xuICAgIGV4dGVuZFN0YXRpY3MoZCwgYik7XG4gICAgZnVuY3Rpb24gX18oKSB7XG4gICAgICB0aGlzLmNvbnN0cnVjdG9yID0gZDtcbiAgICB9XG4gICAgZC5wcm90b3R5cGUgPSBiID09PSBudWxsID8gT2JqZWN0LmNyZWF0ZShiKSA6IChfXy5wcm90b3R5cGUgPSBiLnByb3RvdHlwZSwgbmV3IF9fKCkpO1xuICB9O1xufSgpO1xuT2JqZWN0LmRlZmluZVByb3BlcnR5KGV4cG9ydHMsIFwiX19lc01vZHVsZVwiLCB7XG4gIHZhbHVlOiB0cnVlXG59KTtcbmV4cG9ydHMuSFRNTE1hdGhJdGVtID0gdm9pZCAwO1xudmFyIE1hdGhJdGVtX2pzXzEgPSByZXF1aXJlKFwiLi4vLi4vY29yZS9NYXRoSXRlbS5qc1wiKTtcbnZhciBIVE1MTWF0aEl0ZW0gPSBmdW5jdGlvbiAoX3N1cGVyKSB7XG4gIF9fZXh0ZW5kcyhIVE1MTWF0aEl0ZW0sIF9zdXBlcik7XG4gIGZ1bmN0aW9uIEhUTUxNYXRoSXRlbShtYXRoLCBqYXgsIGRpc3BsYXksIHN0YXJ0LCBlbmQpIHtcbiAgICBpZiAoZGlzcGxheSA9PT0gdm9pZCAwKSB7XG4gICAgICBkaXNwbGF5ID0gdHJ1ZTtcbiAgICB9XG4gICAgaWYgKHN0YXJ0ID09PSB2b2lkIDApIHtcbiAgICAgIHN0YXJ0ID0ge1xuICAgICAgICBub2RlOiBudWxsLFxuICAgICAgICBuOiAwLFxuICAgICAgICBkZWxpbTogJydcbiAgICAgIH07XG4gICAgfVxuICAgIGlmIChlbmQgPT09IHZvaWQgMCkge1xuICAgICAgZW5kID0ge1xuICAgICAgICBub2RlOiBudWxsLFxuICAgICAgICBuOiAwLFxuICAgICAgICBkZWxpbTogJydcbiAgICAgIH07XG4gICAgfVxuICAgIHJldHVybiBfc3VwZXIuY2FsbCh0aGlzLCBtYXRoLCBqYXgsIGRpc3BsYXksIHN0YXJ0LCBlbmQpIHx8IHRoaXM7XG4gIH1cbiAgT2JqZWN0LmRlZmluZVByb3BlcnR5KEhUTUxNYXRoSXRlbS5wcm90b3R5cGUsIFwiYWRhcHRvclwiLCB7XG4gICAgZ2V0OiBmdW5jdGlvbiAoKSB7XG4gICAgICByZXR1cm4gdGhpcy5pbnB1dEpheC5hZGFwdG9yO1xuICAgIH0sXG4gICAgZW51bWVyYWJsZTogZmFsc2UsXG4gICAgY29uZmlndXJhYmxlOiB0cnVlXG4gIH0pO1xuICBIVE1MTWF0aEl0ZW0ucHJvdG90eXBlLnVwZGF0ZURvY3VtZW50ID0gZnVuY3Rpb24gKF9odG1sKSB7XG4gICAgaWYgKHRoaXMuc3RhdGUoKSA8IE1hdGhJdGVtX2pzXzEuU1RBVEUuSU5TRVJURUQpIHtcbiAgICAgIGlmICh0aGlzLmlucHV0SmF4LnByb2Nlc3NTdHJpbmdzKSB7XG4gICAgICAgIHZhciBub2RlID0gdGhpcy5zdGFydC5ub2RlO1xuICAgICAgICBpZiAobm9kZSA9PT0gdGhpcy5lbmQubm9kZSkge1xuICAgICAgICAgIGlmICh0aGlzLmVuZC5uICYmIHRoaXMuZW5kLm4gPCB0aGlzLmFkYXB0b3IudmFsdWUodGhpcy5lbmQubm9kZSkubGVuZ3RoKSB7XG4gICAgICAgICAgICB0aGlzLmFkYXB0b3Iuc3BsaXQodGhpcy5lbmQubm9kZSwgdGhpcy5lbmQubik7XG4gICAgICAgICAgfVxuICAgICAgICAgIGlmICh0aGlzLnN0YXJ0Lm4pIHtcbiAgICAgICAgICAgIG5vZGUgPSB0aGlzLmFkYXB0b3Iuc3BsaXQodGhpcy5zdGFydC5ub2RlLCB0aGlzLnN0YXJ0Lm4pO1xuICAgICAgICAgIH1cbiAgICAgICAgICB0aGlzLmFkYXB0b3IucmVwbGFjZSh0aGlzLnR5cGVzZXRSb290LCBub2RlKTtcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICBpZiAodGhpcy5zdGFydC5uKSB7XG4gICAgICAgICAgICBub2RlID0gdGhpcy5hZGFwdG9yLnNwbGl0KG5vZGUsIHRoaXMuc3RhcnQubik7XG4gICAgICAgICAgfVxuICAgICAgICAgIHdoaWxlIChub2RlICE9PSB0aGlzLmVuZC5ub2RlKSB7XG4gICAgICAgICAgICB2YXIgbmV4dCA9IHRoaXMuYWRhcHRvci5uZXh0KG5vZGUpO1xuICAgICAgICAgICAgdGhpcy5hZGFwdG9yLnJlbW92ZShub2RlKTtcbiAgICAgICAgICAgIG5vZGUgPSBuZXh0O1xuICAgICAgICAgIH1cbiAgICAgICAgICB0aGlzLmFkYXB0b3IuaW5zZXJ0KHRoaXMudHlwZXNldFJvb3QsIG5vZGUpO1xuICAgICAgICAgIGlmICh0aGlzLmVuZC5uIDwgdGhpcy5hZGFwdG9yLnZhbHVlKG5vZGUpLmxlbmd0aCkge1xuICAgICAgICAgICAgdGhpcy5hZGFwdG9yLnNwbGl0KG5vZGUsIHRoaXMuZW5kLm4pO1xuICAgICAgICAgIH1cbiAgICAgICAgICB0aGlzLmFkYXB0b3IucmVtb3ZlKG5vZGUpO1xuICAgICAgICB9XG4gICAgICB9IGVsc2Uge1xuICAgICAgICB0aGlzLmFkYXB0b3IucmVwbGFjZSh0aGlzLnR5cGVzZXRSb290LCB0aGlzLnN0YXJ0Lm5vZGUpO1xuICAgICAgfVxuICAgICAgdGhpcy5zdGFydC5ub2RlID0gdGhpcy5lbmQubm9kZSA9IHRoaXMudHlwZXNldFJvb3Q7XG4gICAgICB0aGlzLnN0YXJ0Lm4gPSB0aGlzLmVuZC5uID0gMDtcbiAgICAgIHRoaXMuc3RhdGUoTWF0aEl0ZW1fanNfMS5TVEFURS5JTlNFUlRFRCk7XG4gICAgfVxuICB9O1xuICBIVE1MTWF0aEl0ZW0ucHJvdG90eXBlLnVwZGF0ZVN0eWxlU2hlZXQgPSBmdW5jdGlvbiAoZG9jdW1lbnQpIHtcbiAgICBkb2N1bWVudC5hZGRTdHlsZVNoZWV0KCk7XG4gIH07XG4gIEhUTUxNYXRoSXRlbS5wcm90b3R5cGUucmVtb3ZlRnJvbURvY3VtZW50ID0gZnVuY3Rpb24gKHJlc3RvcmUpIHtcbiAgICBpZiAocmVzdG9yZSA9PT0gdm9pZCAwKSB7XG4gICAgICByZXN0b3JlID0gZmFsc2U7XG4gICAgfVxuICAgIGlmICh0aGlzLnN0YXRlKCkgPj0gTWF0aEl0ZW1fanNfMS5TVEFURS5UWVBFU0VUKSB7XG4gICAgICB2YXIgYWRhcHRvciA9IHRoaXMuYWRhcHRvcjtcbiAgICAgIHZhciBub2RlID0gdGhpcy5zdGFydC5ub2RlO1xuICAgICAgdmFyIG1hdGggPSBhZGFwdG9yLnRleHQoJycpO1xuICAgICAgaWYgKHJlc3RvcmUpIHtcbiAgICAgICAgdmFyIHRleHQgPSB0aGlzLnN0YXJ0LmRlbGltICsgdGhpcy5tYXRoICsgdGhpcy5lbmQuZGVsaW07XG4gICAgICAgIGlmICh0aGlzLmlucHV0SmF4LnByb2Nlc3NTdHJpbmdzKSB7XG4gICAgICAgICAgbWF0aCA9IGFkYXB0b3IudGV4dCh0ZXh0KTtcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICB2YXIgZG9jID0gYWRhcHRvci5wYXJzZSh0ZXh0LCAndGV4dC9odG1sJyk7XG4gICAgICAgICAgbWF0aCA9IGFkYXB0b3IuZmlyc3RDaGlsZChhZGFwdG9yLmJvZHkoZG9jKSk7XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICAgIGlmIChhZGFwdG9yLnBhcmVudChub2RlKSkge1xuICAgICAgICBhZGFwdG9yLnJlcGxhY2UobWF0aCwgbm9kZSk7XG4gICAgICB9XG4gICAgICB0aGlzLnN0YXJ0Lm5vZGUgPSB0aGlzLmVuZC5ub2RlID0gbWF0aDtcbiAgICAgIHRoaXMuc3RhcnQubiA9IHRoaXMuZW5kLm4gPSAwO1xuICAgIH1cbiAgfTtcbiAgcmV0dXJuIEhUTUxNYXRoSXRlbTtcbn0oTWF0aEl0ZW1fanNfMS5BYnN0cmFjdE1hdGhJdGVtKTtcbmV4cG9ydHMuSFRNTE1hdGhJdGVtID0gSFRNTE1hdGhJdGVtOyIsIlwidXNlIHN0cmljdFwiO1xuXG52YXIgX19leHRlbmRzID0gdGhpcyAmJiB0aGlzLl9fZXh0ZW5kcyB8fCBmdW5jdGlvbiAoKSB7XG4gIHZhciBleHRlbmRTdGF0aWNzID0gZnVuY3Rpb24gKGQsIGIpIHtcbiAgICBleHRlbmRTdGF0aWNzID0gT2JqZWN0LnNldFByb3RvdHlwZU9mIHx8IHtcbiAgICAgIF9fcHJvdG9fXzogW11cbiAgICB9IGluc3RhbmNlb2YgQXJyYXkgJiYgZnVuY3Rpb24gKGQsIGIpIHtcbiAgICAgIGQuX19wcm90b19fID0gYjtcbiAgICB9IHx8IGZ1bmN0aW9uIChkLCBiKSB7XG4gICAgICBmb3IgKHZhciBwIGluIGIpIGlmIChPYmplY3QucHJvdG90eXBlLmhhc093blByb3BlcnR5LmNhbGwoYiwgcCkpIGRbcF0gPSBiW3BdO1xuICAgIH07XG4gICAgcmV0dXJuIGV4dGVuZFN0YXRpY3MoZCwgYik7XG4gIH07XG4gIHJldHVybiBmdW5jdGlvbiAoZCwgYikge1xuICAgIGlmICh0eXBlb2YgYiAhPT0gXCJmdW5jdGlvblwiICYmIGIgIT09IG51bGwpIHRocm93IG5ldyBUeXBlRXJyb3IoXCJDbGFzcyBleHRlbmRzIHZhbHVlIFwiICsgU3RyaW5nKGIpICsgXCIgaXMgbm90IGEgY29uc3RydWN0b3Igb3IgbnVsbFwiKTtcbiAgICBleHRlbmRTdGF0aWNzKGQsIGIpO1xuICAgIGZ1bmN0aW9uIF9fKCkge1xuICAgICAgdGhpcy5jb25zdHJ1Y3RvciA9IGQ7XG4gICAgfVxuICAgIGQucHJvdG90eXBlID0gYiA9PT0gbnVsbCA/IE9iamVjdC5jcmVhdGUoYikgOiAoX18ucHJvdG90eXBlID0gYi5wcm90b3R5cGUsIG5ldyBfXygpKTtcbiAgfTtcbn0oKTtcbk9iamVjdC5kZWZpbmVQcm9wZXJ0eShleHBvcnRzLCBcIl9fZXNNb2R1bGVcIiwge1xuICB2YWx1ZTogdHJ1ZVxufSk7XG5leHBvcnRzLkhUTUxNYXRoTGlzdCA9IHZvaWQgMDtcbnZhciBNYXRoTGlzdF9qc18xID0gcmVxdWlyZShcIi4uLy4uL2NvcmUvTWF0aExpc3QuanNcIik7XG52YXIgSFRNTE1hdGhMaXN0ID0gZnVuY3Rpb24gKF9zdXBlcikge1xuICBfX2V4dGVuZHMoSFRNTE1hdGhMaXN0LCBfc3VwZXIpO1xuICBmdW5jdGlvbiBIVE1MTWF0aExpc3QoKSB7XG4gICAgcmV0dXJuIF9zdXBlciAhPT0gbnVsbCAmJiBfc3VwZXIuYXBwbHkodGhpcywgYXJndW1lbnRzKSB8fCB0aGlzO1xuICB9XG4gIHJldHVybiBIVE1MTWF0aExpc3Q7XG59KE1hdGhMaXN0X2pzXzEuQWJzdHJhY3RNYXRoTGlzdCk7XG5leHBvcnRzLkhUTUxNYXRoTGlzdCA9IEhUTUxNYXRoTGlzdDsiLCJcInVzZSBzdHJpY3RcIjtcblxudmFyIF9fZXh0ZW5kcyA9IHRoaXMgJiYgdGhpcy5fX2V4dGVuZHMgfHwgZnVuY3Rpb24gKCkge1xuICB2YXIgZXh0ZW5kU3RhdGljcyA9IGZ1bmN0aW9uIChkLCBiKSB7XG4gICAgZXh0ZW5kU3RhdGljcyA9IE9iamVjdC5zZXRQcm90b3R5cGVPZiB8fCB7XG4gICAgICBfX3Byb3RvX186IFtdXG4gICAgfSBpbnN0YW5jZW9mIEFycmF5ICYmIGZ1bmN0aW9uIChkLCBiKSB7XG4gICAgICBkLl9fcHJvdG9fXyA9IGI7XG4gICAgfSB8fCBmdW5jdGlvbiAoZCwgYikge1xuICAgICAgZm9yICh2YXIgcCBpbiBiKSBpZiAoT2JqZWN0LnByb3RvdHlwZS5oYXNPd25Qcm9wZXJ0eS5jYWxsKGIsIHApKSBkW3BdID0gYltwXTtcbiAgICB9O1xuICAgIHJldHVybiBleHRlbmRTdGF0aWNzKGQsIGIpO1xuICB9O1xuICByZXR1cm4gZnVuY3Rpb24gKGQsIGIpIHtcbiAgICBpZiAodHlwZW9mIGIgIT09IFwiZnVuY3Rpb25cIiAmJiBiICE9PSBudWxsKSB0aHJvdyBuZXcgVHlwZUVycm9yKFwiQ2xhc3MgZXh0ZW5kcyB2YWx1ZSBcIiArIFN0cmluZyhiKSArIFwiIGlzIG5vdCBhIGNvbnN0cnVjdG9yIG9yIG51bGxcIik7XG4gICAgZXh0ZW5kU3RhdGljcyhkLCBiKTtcbiAgICBmdW5jdGlvbiBfXygpIHtcbiAgICAgIHRoaXMuY29uc3RydWN0b3IgPSBkO1xuICAgIH1cbiAgICBkLnByb3RvdHlwZSA9IGIgPT09IG51bGwgPyBPYmplY3QuY3JlYXRlKGIpIDogKF9fLnByb3RvdHlwZSA9IGIucHJvdG90eXBlLCBuZXcgX18oKSk7XG4gIH07XG59KCk7XG52YXIgX192YWx1ZXMgPSB0aGlzICYmIHRoaXMuX192YWx1ZXMgfHwgZnVuY3Rpb24gKG8pIHtcbiAgdmFyIHMgPSB0eXBlb2YgU3ltYm9sID09PSBcImZ1bmN0aW9uXCIgJiYgU3ltYm9sLml0ZXJhdG9yLFxuICAgIG0gPSBzICYmIG9bc10sXG4gICAgaSA9IDA7XG4gIGlmIChtKSByZXR1cm4gbS5jYWxsKG8pO1xuICBpZiAobyAmJiB0eXBlb2Ygby5sZW5ndGggPT09IFwibnVtYmVyXCIpIHJldHVybiB7XG4gICAgbmV4dDogZnVuY3Rpb24gKCkge1xuICAgICAgaWYgKG8gJiYgaSA+PSBvLmxlbmd0aCkgbyA9IHZvaWQgMDtcbiAgICAgIHJldHVybiB7XG4gICAgICAgIHZhbHVlOiBvICYmIG9baSsrXSxcbiAgICAgICAgZG9uZTogIW9cbiAgICAgIH07XG4gICAgfVxuICB9O1xuICB0aHJvdyBuZXcgVHlwZUVycm9yKHMgPyBcIk9iamVjdCBpcyBub3QgaXRlcmFibGUuXCIgOiBcIlN5bWJvbC5pdGVyYXRvciBpcyBub3QgZGVmaW5lZC5cIik7XG59O1xudmFyIF9fcmVhZCA9IHRoaXMgJiYgdGhpcy5fX3JlYWQgfHwgZnVuY3Rpb24gKG8sIG4pIHtcbiAgdmFyIG0gPSB0eXBlb2YgU3ltYm9sID09PSBcImZ1bmN0aW9uXCIgJiYgb1tTeW1ib2wuaXRlcmF0b3JdO1xuICBpZiAoIW0pIHJldHVybiBvO1xuICB2YXIgaSA9IG0uY2FsbChvKSxcbiAgICByLFxuICAgIGFyID0gW10sXG4gICAgZTtcbiAgdHJ5IHtcbiAgICB3aGlsZSAoKG4gPT09IHZvaWQgMCB8fCBuLS0gPiAwKSAmJiAhKHIgPSBpLm5leHQoKSkuZG9uZSkgYXIucHVzaChyLnZhbHVlKTtcbiAgfSBjYXRjaCAoZXJyb3IpIHtcbiAgICBlID0ge1xuICAgICAgZXJyb3I6IGVycm9yXG4gICAgfTtcbiAgfSBmaW5hbGx5IHtcbiAgICB0cnkge1xuICAgICAgaWYgKHIgJiYgIXIuZG9uZSAmJiAobSA9IGlbXCJyZXR1cm5cIl0pKSBtLmNhbGwoaSk7XG4gICAgfSBmaW5hbGx5IHtcbiAgICAgIGlmIChlKSB0aHJvdyBlLmVycm9yO1xuICAgIH1cbiAgfVxuICByZXR1cm4gYXI7XG59O1xudmFyIF9fc3ByZWFkQXJyYXkgPSB0aGlzICYmIHRoaXMuX19zcHJlYWRBcnJheSB8fCBmdW5jdGlvbiAodG8sIGZyb20sIHBhY2spIHtcbiAgaWYgKHBhY2sgfHwgYXJndW1lbnRzLmxlbmd0aCA9PT0gMikgZm9yICh2YXIgaSA9IDAsIGwgPSBmcm9tLmxlbmd0aCwgYXI7IGkgPCBsOyBpKyspIHtcbiAgICBpZiAoYXIgfHwgIShpIGluIGZyb20pKSB7XG4gICAgICBpZiAoIWFyKSBhciA9IEFycmF5LnByb3RvdHlwZS5zbGljZS5jYWxsKGZyb20sIDAsIGkpO1xuICAgICAgYXJbaV0gPSBmcm9tW2ldO1xuICAgIH1cbiAgfVxuICByZXR1cm4gdG8uY29uY2F0KGFyIHx8IEFycmF5LnByb3RvdHlwZS5zbGljZS5jYWxsKGZyb20pKTtcbn07XG5PYmplY3QuZGVmaW5lUHJvcGVydHkoZXhwb3J0cywgXCJfX2VzTW9kdWxlXCIsIHtcbiAgdmFsdWU6IHRydWVcbn0pO1xuZXhwb3J0cy5CaXRGaWVsZENsYXNzID0gZXhwb3J0cy5CaXRGaWVsZCA9IHZvaWQgMDtcbnZhciBCaXRGaWVsZCA9IGZ1bmN0aW9uICgpIHtcbiAgZnVuY3Rpb24gQml0RmllbGQoKSB7XG4gICAgdGhpcy5iaXRzID0gMDtcbiAgfVxuICBCaXRGaWVsZC5hbGxvY2F0ZSA9IGZ1bmN0aW9uICgpIHtcbiAgICB2YXIgZV8xLCBfYTtcbiAgICB2YXIgbmFtZXMgPSBbXTtcbiAgICBmb3IgKHZhciBfaSA9IDA7IF9pIDwgYXJndW1lbnRzLmxlbmd0aDsgX2krKykge1xuICAgICAgbmFtZXNbX2ldID0gYXJndW1lbnRzW19pXTtcbiAgICB9XG4gICAgdHJ5IHtcbiAgICAgIGZvciAodmFyIG5hbWVzXzEgPSBfX3ZhbHVlcyhuYW1lcyksIG5hbWVzXzFfMSA9IG5hbWVzXzEubmV4dCgpOyAhbmFtZXNfMV8xLmRvbmU7IG5hbWVzXzFfMSA9IG5hbWVzXzEubmV4dCgpKSB7XG4gICAgICAgIHZhciBuYW1lXzEgPSBuYW1lc18xXzEudmFsdWU7XG4gICAgICAgIGlmICh0aGlzLmhhcyhuYW1lXzEpKSB7XG4gICAgICAgICAgdGhyb3cgbmV3IEVycm9yKCdCaXQgYWxyZWFkeSBhbGxvY2F0ZWQgZm9yICcgKyBuYW1lXzEpO1xuICAgICAgICB9XG4gICAgICAgIGlmICh0aGlzLm5leHQgPT09IEJpdEZpZWxkLk1BWEJJVCkge1xuICAgICAgICAgIHRocm93IG5ldyBFcnJvcignTWF4aW11bSBudW1iZXIgb2YgYml0cyBhbHJlYWR5IGFsbG9jYXRlZCcpO1xuICAgICAgICB9XG4gICAgICAgIHRoaXMubmFtZXMuc2V0KG5hbWVfMSwgdGhpcy5uZXh0KTtcbiAgICAgICAgdGhpcy5uZXh0IDw8PSAxO1xuICAgICAgfVxuICAgIH0gY2F0Y2ggKGVfMV8xKSB7XG4gICAgICBlXzEgPSB7XG4gICAgICAgIGVycm9yOiBlXzFfMVxuICAgICAgfTtcbiAgICB9IGZpbmFsbHkge1xuICAgICAgdHJ5IHtcbiAgICAgICAgaWYgKG5hbWVzXzFfMSAmJiAhbmFtZXNfMV8xLmRvbmUgJiYgKF9hID0gbmFtZXNfMS5yZXR1cm4pKSBfYS5jYWxsKG5hbWVzXzEpO1xuICAgICAgfSBmaW5hbGx5IHtcbiAgICAgICAgaWYgKGVfMSkgdGhyb3cgZV8xLmVycm9yO1xuICAgICAgfVxuICAgIH1cbiAgfTtcbiAgQml0RmllbGQuaGFzID0gZnVuY3Rpb24gKG5hbWUpIHtcbiAgICByZXR1cm4gdGhpcy5uYW1lcy5oYXMobmFtZSk7XG4gIH07XG4gIEJpdEZpZWxkLnByb3RvdHlwZS5zZXQgPSBmdW5jdGlvbiAobmFtZSkge1xuICAgIHRoaXMuYml0cyB8PSB0aGlzLmdldEJpdChuYW1lKTtcbiAgfTtcbiAgQml0RmllbGQucHJvdG90eXBlLmNsZWFyID0gZnVuY3Rpb24gKG5hbWUpIHtcbiAgICB0aGlzLmJpdHMgJj0gfnRoaXMuZ2V0Qml0KG5hbWUpO1xuICB9O1xuICBCaXRGaWVsZC5wcm90b3R5cGUuaXNTZXQgPSBmdW5jdGlvbiAobmFtZSkge1xuICAgIHJldHVybiAhISh0aGlzLmJpdHMgJiB0aGlzLmdldEJpdChuYW1lKSk7XG4gIH07XG4gIEJpdEZpZWxkLnByb3RvdHlwZS5yZXNldCA9IGZ1bmN0aW9uICgpIHtcbiAgICB0aGlzLmJpdHMgPSAwO1xuICB9O1xuICBCaXRGaWVsZC5wcm90b3R5cGUuZ2V0Qml0ID0gZnVuY3Rpb24gKG5hbWUpIHtcbiAgICB2YXIgYml0ID0gdGhpcy5jb25zdHJ1Y3Rvci5uYW1lcy5nZXQobmFtZSk7XG4gICAgaWYgKCFiaXQpIHtcbiAgICAgIHRocm93IG5ldyBFcnJvcignVW5rbm93biBiaXQtZmllbGQgbmFtZTogJyArIG5hbWUpO1xuICAgIH1cbiAgICByZXR1cm4gYml0O1xuICB9O1xuICBCaXRGaWVsZC5NQVhCSVQgPSAxIDw8IDMxO1xuICBCaXRGaWVsZC5uZXh0ID0gMTtcbiAgQml0RmllbGQubmFtZXMgPSBuZXcgTWFwKCk7XG4gIHJldHVybiBCaXRGaWVsZDtcbn0oKTtcbmV4cG9ydHMuQml0RmllbGQgPSBCaXRGaWVsZDtcbmZ1bmN0aW9uIEJpdEZpZWxkQ2xhc3MoKSB7XG4gIHZhciBuYW1lcyA9IFtdO1xuICBmb3IgKHZhciBfaSA9IDA7IF9pIDwgYXJndW1lbnRzLmxlbmd0aDsgX2krKykge1xuICAgIG5hbWVzW19pXSA9IGFyZ3VtZW50c1tfaV07XG4gIH1cbiAgdmFyIEJpdHMgPSBmdW5jdGlvbiAoX3N1cGVyKSB7XG4gICAgX19leHRlbmRzKEJpdHMsIF9zdXBlcik7XG4gICAgZnVuY3Rpb24gQml0cygpIHtcbiAgICAgIHJldHVybiBfc3VwZXIgIT09IG51bGwgJiYgX3N1cGVyLmFwcGx5KHRoaXMsIGFyZ3VtZW50cykgfHwgdGhpcztcbiAgICB9XG4gICAgcmV0dXJuIEJpdHM7XG4gIH0oQml0RmllbGQpO1xuICBCaXRzLmFsbG9jYXRlLmFwcGx5KEJpdHMsIF9fc3ByZWFkQXJyYXkoW10sIF9fcmVhZChuYW1lcyksIGZhbHNlKSk7XG4gIHJldHVybiBCaXRzO1xufVxuZXhwb3J0cy5CaXRGaWVsZENsYXNzID0gQml0RmllbGRDbGFzczsiLCJcInVzZSBzdHJpY3RcIjtcblxudmFyIF9fZXh0ZW5kcyA9IHRoaXMgJiYgdGhpcy5fX2V4dGVuZHMgfHwgZnVuY3Rpb24gKCkge1xuICB2YXIgZXh0ZW5kU3RhdGljcyA9IGZ1bmN0aW9uIChkLCBiKSB7XG4gICAgZXh0ZW5kU3RhdGljcyA9IE9iamVjdC5zZXRQcm90b3R5cGVPZiB8fCB7XG4gICAgICBfX3Byb3RvX186IFtdXG4gICAgfSBpbnN0YW5jZW9mIEFycmF5ICYmIGZ1bmN0aW9uIChkLCBiKSB7XG4gICAgICBkLl9fcHJvdG9fXyA9IGI7XG4gICAgfSB8fCBmdW5jdGlvbiAoZCwgYikge1xuICAgICAgZm9yICh2YXIgcCBpbiBiKSBpZiAoT2JqZWN0LnByb3RvdHlwZS5oYXNPd25Qcm9wZXJ0eS5jYWxsKGIsIHApKSBkW3BdID0gYltwXTtcbiAgICB9O1xuICAgIHJldHVybiBleHRlbmRTdGF0aWNzKGQsIGIpO1xuICB9O1xuICByZXR1cm4gZnVuY3Rpb24gKGQsIGIpIHtcbiAgICBpZiAodHlwZW9mIGIgIT09IFwiZnVuY3Rpb25cIiAmJiBiICE9PSBudWxsKSB0aHJvdyBuZXcgVHlwZUVycm9yKFwiQ2xhc3MgZXh0ZW5kcyB2YWx1ZSBcIiArIFN0cmluZyhiKSArIFwiIGlzIG5vdCBhIGNvbnN0cnVjdG9yIG9yIG51bGxcIik7XG4gICAgZXh0ZW5kU3RhdGljcyhkLCBiKTtcbiAgICBmdW5jdGlvbiBfXygpIHtcbiAgICAgIHRoaXMuY29uc3RydWN0b3IgPSBkO1xuICAgIH1cbiAgICBkLnByb3RvdHlwZSA9IGIgPT09IG51bGwgPyBPYmplY3QuY3JlYXRlKGIpIDogKF9fLnByb3RvdHlwZSA9IGIucHJvdG90eXBlLCBuZXcgX18oKSk7XG4gIH07XG59KCk7XG52YXIgX192YWx1ZXMgPSB0aGlzICYmIHRoaXMuX192YWx1ZXMgfHwgZnVuY3Rpb24gKG8pIHtcbiAgdmFyIHMgPSB0eXBlb2YgU3ltYm9sID09PSBcImZ1bmN0aW9uXCIgJiYgU3ltYm9sLml0ZXJhdG9yLFxuICAgIG0gPSBzICYmIG9bc10sXG4gICAgaSA9IDA7XG4gIGlmIChtKSByZXR1cm4gbS5jYWxsKG8pO1xuICBpZiAobyAmJiB0eXBlb2Ygby5sZW5ndGggPT09IFwibnVtYmVyXCIpIHJldHVybiB7XG4gICAgbmV4dDogZnVuY3Rpb24gKCkge1xuICAgICAgaWYgKG8gJiYgaSA+PSBvLmxlbmd0aCkgbyA9IHZvaWQgMDtcbiAgICAgIHJldHVybiB7XG4gICAgICAgIHZhbHVlOiBvICYmIG9baSsrXSxcbiAgICAgICAgZG9uZTogIW9cbiAgICAgIH07XG4gICAgfVxuICB9O1xuICB0aHJvdyBuZXcgVHlwZUVycm9yKHMgPyBcIk9iamVjdCBpcyBub3QgaXRlcmFibGUuXCIgOiBcIlN5bWJvbC5pdGVyYXRvciBpcyBub3QgZGVmaW5lZC5cIik7XG59O1xudmFyIF9fcmVhZCA9IHRoaXMgJiYgdGhpcy5fX3JlYWQgfHwgZnVuY3Rpb24gKG8sIG4pIHtcbiAgdmFyIG0gPSB0eXBlb2YgU3ltYm9sID09PSBcImZ1bmN0aW9uXCIgJiYgb1tTeW1ib2wuaXRlcmF0b3JdO1xuICBpZiAoIW0pIHJldHVybiBvO1xuICB2YXIgaSA9IG0uY2FsbChvKSxcbiAgICByLFxuICAgIGFyID0gW10sXG4gICAgZTtcbiAgdHJ5IHtcbiAgICB3aGlsZSAoKG4gPT09IHZvaWQgMCB8fCBuLS0gPiAwKSAmJiAhKHIgPSBpLm5leHQoKSkuZG9uZSkgYXIucHVzaChyLnZhbHVlKTtcbiAgfSBjYXRjaCAoZXJyb3IpIHtcbiAgICBlID0ge1xuICAgICAgZXJyb3I6IGVycm9yXG4gICAgfTtcbiAgfSBmaW5hbGx5IHtcbiAgICB0cnkge1xuICAgICAgaWYgKHIgJiYgIXIuZG9uZSAmJiAobSA9IGlbXCJyZXR1cm5cIl0pKSBtLmNhbGwoaSk7XG4gICAgfSBmaW5hbGx5IHtcbiAgICAgIGlmIChlKSB0aHJvdyBlLmVycm9yO1xuICAgIH1cbiAgfVxuICByZXR1cm4gYXI7XG59O1xudmFyIF9fc3ByZWFkQXJyYXkgPSB0aGlzICYmIHRoaXMuX19zcHJlYWRBcnJheSB8fCBmdW5jdGlvbiAodG8sIGZyb20sIHBhY2spIHtcbiAgaWYgKHBhY2sgfHwgYXJndW1lbnRzLmxlbmd0aCA9PT0gMikgZm9yICh2YXIgaSA9IDAsIGwgPSBmcm9tLmxlbmd0aCwgYXI7IGkgPCBsOyBpKyspIHtcbiAgICBpZiAoYXIgfHwgIShpIGluIGZyb20pKSB7XG4gICAgICBpZiAoIWFyKSBhciA9IEFycmF5LnByb3RvdHlwZS5zbGljZS5jYWxsKGZyb20sIDAsIGkpO1xuICAgICAgYXJbaV0gPSBmcm9tW2ldO1xuICAgIH1cbiAgfVxuICByZXR1cm4gdG8uY29uY2F0KGFyIHx8IEFycmF5LnByb3RvdHlwZS5zbGljZS5jYWxsKGZyb20pKTtcbn07XG5PYmplY3QuZGVmaW5lUHJvcGVydHkoZXhwb3J0cywgXCJfX2VzTW9kdWxlXCIsIHtcbiAgdmFsdWU6IHRydWVcbn0pO1xuZXhwb3J0cy5GdW5jdGlvbkxpc3QgPSB2b2lkIDA7XG52YXIgUHJpb3JpdGl6ZWRMaXN0X2pzXzEgPSByZXF1aXJlKFwiLi9Qcmlvcml0aXplZExpc3QuanNcIik7XG52YXIgRnVuY3Rpb25MaXN0ID0gZnVuY3Rpb24gKF9zdXBlcikge1xuICBfX2V4dGVuZHMoRnVuY3Rpb25MaXN0LCBfc3VwZXIpO1xuICBmdW5jdGlvbiBGdW5jdGlvbkxpc3QoKSB7XG4gICAgcmV0dXJuIF9zdXBlciAhPT0gbnVsbCAmJiBfc3VwZXIuYXBwbHkodGhpcywgYXJndW1lbnRzKSB8fCB0aGlzO1xuICB9XG4gIEZ1bmN0aW9uTGlzdC5wcm90b3R5cGUuZXhlY3V0ZSA9IGZ1bmN0aW9uICgpIHtcbiAgICB2YXIgZV8xLCBfYTtcbiAgICB2YXIgZGF0YSA9IFtdO1xuICAgIGZvciAodmFyIF9pID0gMDsgX2kgPCBhcmd1bWVudHMubGVuZ3RoOyBfaSsrKSB7XG4gICAgICBkYXRhW19pXSA9IGFyZ3VtZW50c1tfaV07XG4gICAgfVxuICAgIHRyeSB7XG4gICAgICBmb3IgKHZhciBfYiA9IF9fdmFsdWVzKHRoaXMpLCBfYyA9IF9iLm5leHQoKTsgIV9jLmRvbmU7IF9jID0gX2IubmV4dCgpKSB7XG4gICAgICAgIHZhciBpdGVtID0gX2MudmFsdWU7XG4gICAgICAgIHZhciByZXN1bHQgPSBpdGVtLml0ZW0uYXBwbHkoaXRlbSwgX19zcHJlYWRBcnJheShbXSwgX19yZWFkKGRhdGEpLCBmYWxzZSkpO1xuICAgICAgICBpZiAocmVzdWx0ID09PSBmYWxzZSkge1xuICAgICAgICAgIHJldHVybiBmYWxzZTtcbiAgICAgICAgfVxuICAgICAgfVxuICAgIH0gY2F0Y2ggKGVfMV8xKSB7XG4gICAgICBlXzEgPSB7XG4gICAgICAgIGVycm9yOiBlXzFfMVxuICAgICAgfTtcbiAgICB9IGZpbmFsbHkge1xuICAgICAgdHJ5IHtcbiAgICAgICAgaWYgKF9jICYmICFfYy5kb25lICYmIChfYSA9IF9iLnJldHVybikpIF9hLmNhbGwoX2IpO1xuICAgICAgfSBmaW5hbGx5IHtcbiAgICAgICAgaWYgKGVfMSkgdGhyb3cgZV8xLmVycm9yO1xuICAgICAgfVxuICAgIH1cbiAgICByZXR1cm4gdHJ1ZTtcbiAgfTtcbiAgRnVuY3Rpb25MaXN0LnByb3RvdHlwZS5hc3luY0V4ZWN1dGUgPSBmdW5jdGlvbiAoKSB7XG4gICAgdmFyIGRhdGEgPSBbXTtcbiAgICBmb3IgKHZhciBfaSA9IDA7IF9pIDwgYXJndW1lbnRzLmxlbmd0aDsgX2krKykge1xuICAgICAgZGF0YVtfaV0gPSBhcmd1bWVudHNbX2ldO1xuICAgIH1cbiAgICB2YXIgaSA9IC0xO1xuICAgIHZhciBpdGVtcyA9IHRoaXMuaXRlbXM7XG4gICAgcmV0dXJuIG5ldyBQcm9taXNlKGZ1bmN0aW9uIChvaywgZmFpbCkge1xuICAgICAgKGZ1bmN0aW9uIGV4ZWN1dGUoKSB7XG4gICAgICAgIHZhciBfYTtcbiAgICAgICAgd2hpbGUgKCsraSA8IGl0ZW1zLmxlbmd0aCkge1xuICAgICAgICAgIHZhciByZXN1bHQgPSAoX2EgPSBpdGVtc1tpXSkuaXRlbS5hcHBseShfYSwgX19zcHJlYWRBcnJheShbXSwgX19yZWFkKGRhdGEpLCBmYWxzZSkpO1xuICAgICAgICAgIGlmIChyZXN1bHQgaW5zdGFuY2VvZiBQcm9taXNlKSB7XG4gICAgICAgICAgICByZXN1bHQudGhlbihleGVjdXRlKS5jYXRjaChmdW5jdGlvbiAoZXJyKSB7XG4gICAgICAgICAgICAgIHJldHVybiBmYWlsKGVycik7XG4gICAgICAgICAgICB9KTtcbiAgICAgICAgICAgIHJldHVybjtcbiAgICAgICAgICB9XG4gICAgICAgICAgaWYgKHJlc3VsdCA9PT0gZmFsc2UpIHtcbiAgICAgICAgICAgIG9rKGZhbHNlKTtcbiAgICAgICAgICAgIHJldHVybjtcbiAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICAgICAgb2sodHJ1ZSk7XG4gICAgICB9KSgpO1xuICAgIH0pO1xuICB9O1xuICByZXR1cm4gRnVuY3Rpb25MaXN0O1xufShQcmlvcml0aXplZExpc3RfanNfMS5Qcmlvcml0aXplZExpc3QpO1xuZXhwb3J0cy5GdW5jdGlvbkxpc3QgPSBGdW5jdGlvbkxpc3Q7IiwiXCJ1c2Ugc3RyaWN0XCI7XG5cbnZhciBfX2dlbmVyYXRvciA9IHRoaXMgJiYgdGhpcy5fX2dlbmVyYXRvciB8fCBmdW5jdGlvbiAodGhpc0FyZywgYm9keSkge1xuICB2YXIgXyA9IHtcbiAgICAgIGxhYmVsOiAwLFxuICAgICAgc2VudDogZnVuY3Rpb24gKCkge1xuICAgICAgICBpZiAodFswXSAmIDEpIHRocm93IHRbMV07XG4gICAgICAgIHJldHVybiB0WzFdO1xuICAgICAgfSxcbiAgICAgIHRyeXM6IFtdLFxuICAgICAgb3BzOiBbXVxuICAgIH0sXG4gICAgZixcbiAgICB5LFxuICAgIHQsXG4gICAgZztcbiAgcmV0dXJuIGcgPSB7XG4gICAgbmV4dDogdmVyYigwKSxcbiAgICBcInRocm93XCI6IHZlcmIoMSksXG4gICAgXCJyZXR1cm5cIjogdmVyYigyKVxuICB9LCB0eXBlb2YgU3ltYm9sID09PSBcImZ1bmN0aW9uXCIgJiYgKGdbU3ltYm9sLml0ZXJhdG9yXSA9IGZ1bmN0aW9uICgpIHtcbiAgICByZXR1cm4gdGhpcztcbiAgfSksIGc7XG4gIGZ1bmN0aW9uIHZlcmIobikge1xuICAgIHJldHVybiBmdW5jdGlvbiAodikge1xuICAgICAgcmV0dXJuIHN0ZXAoW24sIHZdKTtcbiAgICB9O1xuICB9XG4gIGZ1bmN0aW9uIHN0ZXAob3ApIHtcbiAgICBpZiAoZikgdGhyb3cgbmV3IFR5cGVFcnJvcihcIkdlbmVyYXRvciBpcyBhbHJlYWR5IGV4ZWN1dGluZy5cIik7XG4gICAgd2hpbGUgKF8pIHRyeSB7XG4gICAgICBpZiAoZiA9IDEsIHkgJiYgKHQgPSBvcFswXSAmIDIgPyB5W1wicmV0dXJuXCJdIDogb3BbMF0gPyB5W1widGhyb3dcIl0gfHwgKCh0ID0geVtcInJldHVyblwiXSkgJiYgdC5jYWxsKHkpLCAwKSA6IHkubmV4dCkgJiYgISh0ID0gdC5jYWxsKHksIG9wWzFdKSkuZG9uZSkgcmV0dXJuIHQ7XG4gICAgICBpZiAoeSA9IDAsIHQpIG9wID0gW29wWzBdICYgMiwgdC52YWx1ZV07XG4gICAgICBzd2l0Y2ggKG9wWzBdKSB7XG4gICAgICAgIGNhc2UgMDpcbiAgICAgICAgY2FzZSAxOlxuICAgICAgICAgIHQgPSBvcDtcbiAgICAgICAgICBicmVhaztcbiAgICAgICAgY2FzZSA0OlxuICAgICAgICAgIF8ubGFiZWwrKztcbiAgICAgICAgICByZXR1cm4ge1xuICAgICAgICAgICAgdmFsdWU6IG9wWzFdLFxuICAgICAgICAgICAgZG9uZTogZmFsc2VcbiAgICAgICAgICB9O1xuICAgICAgICBjYXNlIDU6XG4gICAgICAgICAgXy5sYWJlbCsrO1xuICAgICAgICAgIHkgPSBvcFsxXTtcbiAgICAgICAgICBvcCA9IFswXTtcbiAgICAgICAgICBjb250aW51ZTtcbiAgICAgICAgY2FzZSA3OlxuICAgICAgICAgIG9wID0gXy5vcHMucG9wKCk7XG4gICAgICAgICAgXy50cnlzLnBvcCgpO1xuICAgICAgICAgIGNvbnRpbnVlO1xuICAgICAgICBkZWZhdWx0OlxuICAgICAgICAgIGlmICghKHQgPSBfLnRyeXMsIHQgPSB0Lmxlbmd0aCA+IDAgJiYgdFt0Lmxlbmd0aCAtIDFdKSAmJiAob3BbMF0gPT09IDYgfHwgb3BbMF0gPT09IDIpKSB7XG4gICAgICAgICAgICBfID0gMDtcbiAgICAgICAgICAgIGNvbnRpbnVlO1xuICAgICAgICAgIH1cbiAgICAgICAgICBpZiAob3BbMF0gPT09IDMgJiYgKCF0IHx8IG9wWzFdID4gdFswXSAmJiBvcFsxXSA8IHRbM10pKSB7XG4gICAgICAgICAgICBfLmxhYmVsID0gb3BbMV07XG4gICAgICAgICAgICBicmVhaztcbiAgICAgICAgICB9XG4gICAgICAgICAgaWYgKG9wWzBdID09PSA2ICYmIF8ubGFiZWwgPCB0WzFdKSB7XG4gICAgICAgICAgICBfLmxhYmVsID0gdFsxXTtcbiAgICAgICAgICAgIHQgPSBvcDtcbiAgICAgICAgICAgIGJyZWFrO1xuICAgICAgICAgIH1cbiAgICAgICAgICBpZiAodCAmJiBfLmxhYmVsIDwgdFsyXSkge1xuICAgICAgICAgICAgXy5sYWJlbCA9IHRbMl07XG4gICAgICAgICAgICBfLm9wcy5wdXNoKG9wKTtcbiAgICAgICAgICAgIGJyZWFrO1xuICAgICAgICAgIH1cbiAgICAgICAgICBpZiAodFsyXSkgXy5vcHMucG9wKCk7XG4gICAgICAgICAgXy50cnlzLnBvcCgpO1xuICAgICAgICAgIGNvbnRpbnVlO1xuICAgICAgfVxuICAgICAgb3AgPSBib2R5LmNhbGwodGhpc0FyZywgXyk7XG4gICAgfSBjYXRjaCAoZSkge1xuICAgICAgb3AgPSBbNiwgZV07XG4gICAgICB5ID0gMDtcbiAgICB9IGZpbmFsbHkge1xuICAgICAgZiA9IHQgPSAwO1xuICAgIH1cbiAgICBpZiAob3BbMF0gJiA1KSB0aHJvdyBvcFsxXTtcbiAgICByZXR1cm4ge1xuICAgICAgdmFsdWU6IG9wWzBdID8gb3BbMV0gOiB2b2lkIDAsXG4gICAgICBkb25lOiB0cnVlXG4gICAgfTtcbiAgfVxufTtcbnZhciBfX3JlYWQgPSB0aGlzICYmIHRoaXMuX19yZWFkIHx8IGZ1bmN0aW9uIChvLCBuKSB7XG4gIHZhciBtID0gdHlwZW9mIFN5bWJvbCA9PT0gXCJmdW5jdGlvblwiICYmIG9bU3ltYm9sLml0ZXJhdG9yXTtcbiAgaWYgKCFtKSByZXR1cm4gbztcbiAgdmFyIGkgPSBtLmNhbGwobyksXG4gICAgcixcbiAgICBhciA9IFtdLFxuICAgIGU7XG4gIHRyeSB7XG4gICAgd2hpbGUgKChuID09PSB2b2lkIDAgfHwgbi0tID4gMCkgJiYgIShyID0gaS5uZXh0KCkpLmRvbmUpIGFyLnB1c2goci52YWx1ZSk7XG4gIH0gY2F0Y2ggKGVycm9yKSB7XG4gICAgZSA9IHtcbiAgICAgIGVycm9yOiBlcnJvclxuICAgIH07XG4gIH0gZmluYWxseSB7XG4gICAgdHJ5IHtcbiAgICAgIGlmIChyICYmICFyLmRvbmUgJiYgKG0gPSBpW1wicmV0dXJuXCJdKSkgbS5jYWxsKGkpO1xuICAgIH0gZmluYWxseSB7XG4gICAgICBpZiAoZSkgdGhyb3cgZS5lcnJvcjtcbiAgICB9XG4gIH1cbiAgcmV0dXJuIGFyO1xufTtcbnZhciBfX3NwcmVhZEFycmF5ID0gdGhpcyAmJiB0aGlzLl9fc3ByZWFkQXJyYXkgfHwgZnVuY3Rpb24gKHRvLCBmcm9tLCBwYWNrKSB7XG4gIGlmIChwYWNrIHx8IGFyZ3VtZW50cy5sZW5ndGggPT09IDIpIGZvciAodmFyIGkgPSAwLCBsID0gZnJvbS5sZW5ndGgsIGFyOyBpIDwgbDsgaSsrKSB7XG4gICAgaWYgKGFyIHx8ICEoaSBpbiBmcm9tKSkge1xuICAgICAgaWYgKCFhcikgYXIgPSBBcnJheS5wcm90b3R5cGUuc2xpY2UuY2FsbChmcm9tLCAwLCBpKTtcbiAgICAgIGFyW2ldID0gZnJvbVtpXTtcbiAgICB9XG4gIH1cbiAgcmV0dXJuIHRvLmNvbmNhdChhciB8fCBBcnJheS5wcm90b3R5cGUuc2xpY2UuY2FsbChmcm9tKSk7XG59O1xudmFyIF9fdmFsdWVzID0gdGhpcyAmJiB0aGlzLl9fdmFsdWVzIHx8IGZ1bmN0aW9uIChvKSB7XG4gIHZhciBzID0gdHlwZW9mIFN5bWJvbCA9PT0gXCJmdW5jdGlvblwiICYmIFN5bWJvbC5pdGVyYXRvcixcbiAgICBtID0gcyAmJiBvW3NdLFxuICAgIGkgPSAwO1xuICBpZiAobSkgcmV0dXJuIG0uY2FsbChvKTtcbiAgaWYgKG8gJiYgdHlwZW9mIG8ubGVuZ3RoID09PSBcIm51bWJlclwiKSByZXR1cm4ge1xuICAgIG5leHQ6IGZ1bmN0aW9uICgpIHtcbiAgICAgIGlmIChvICYmIGkgPj0gby5sZW5ndGgpIG8gPSB2b2lkIDA7XG4gICAgICByZXR1cm4ge1xuICAgICAgICB2YWx1ZTogbyAmJiBvW2krK10sXG4gICAgICAgIGRvbmU6ICFvXG4gICAgICB9O1xuICAgIH1cbiAgfTtcbiAgdGhyb3cgbmV3IFR5cGVFcnJvcihzID8gXCJPYmplY3QgaXMgbm90IGl0ZXJhYmxlLlwiIDogXCJTeW1ib2wuaXRlcmF0b3IgaXMgbm90IGRlZmluZWQuXCIpO1xufTtcbk9iamVjdC5kZWZpbmVQcm9wZXJ0eShleHBvcnRzLCBcIl9fZXNNb2R1bGVcIiwge1xuICB2YWx1ZTogdHJ1ZVxufSk7XG5leHBvcnRzLkxpbmtlZExpc3QgPSBleHBvcnRzLkxpc3RJdGVtID0gZXhwb3J0cy5FTkQgPSB2b2lkIDA7XG5leHBvcnRzLkVORCA9IFN5bWJvbCgpO1xudmFyIExpc3RJdGVtID0gZnVuY3Rpb24gKCkge1xuICBmdW5jdGlvbiBMaXN0SXRlbShkYXRhKSB7XG4gICAgaWYgKGRhdGEgPT09IHZvaWQgMCkge1xuICAgICAgZGF0YSA9IG51bGw7XG4gICAgfVxuICAgIHRoaXMubmV4dCA9IG51bGw7XG4gICAgdGhpcy5wcmV2ID0gbnVsbDtcbiAgICB0aGlzLmRhdGEgPSBkYXRhO1xuICB9XG4gIHJldHVybiBMaXN0SXRlbTtcbn0oKTtcbmV4cG9ydHMuTGlzdEl0ZW0gPSBMaXN0SXRlbTtcbnZhciBMaW5rZWRMaXN0ID0gZnVuY3Rpb24gKCkge1xuICBmdW5jdGlvbiBMaW5rZWRMaXN0KCkge1xuICAgIHZhciBhcmdzID0gW107XG4gICAgZm9yICh2YXIgX2kgPSAwOyBfaSA8IGFyZ3VtZW50cy5sZW5ndGg7IF9pKyspIHtcbiAgICAgIGFyZ3NbX2ldID0gYXJndW1lbnRzW19pXTtcbiAgICB9XG4gICAgdGhpcy5saXN0ID0gbmV3IExpc3RJdGVtKGV4cG9ydHMuRU5EKTtcbiAgICB0aGlzLmxpc3QubmV4dCA9IHRoaXMubGlzdC5wcmV2ID0gdGhpcy5saXN0O1xuICAgIHRoaXMucHVzaC5hcHBseSh0aGlzLCBfX3NwcmVhZEFycmF5KFtdLCBfX3JlYWQoYXJncyksIGZhbHNlKSk7XG4gIH1cbiAgTGlua2VkTGlzdC5wcm90b3R5cGUuaXNCZWZvcmUgPSBmdW5jdGlvbiAoYSwgYikge1xuICAgIHJldHVybiBhIDwgYjtcbiAgfTtcbiAgTGlua2VkTGlzdC5wcm90b3R5cGUucHVzaCA9IGZ1bmN0aW9uICgpIHtcbiAgICB2YXIgZV8xLCBfYTtcbiAgICB2YXIgYXJncyA9IFtdO1xuICAgIGZvciAodmFyIF9pID0gMDsgX2kgPCBhcmd1bWVudHMubGVuZ3RoOyBfaSsrKSB7XG4gICAgICBhcmdzW19pXSA9IGFyZ3VtZW50c1tfaV07XG4gICAgfVxuICAgIHRyeSB7XG4gICAgICBmb3IgKHZhciBhcmdzXzEgPSBfX3ZhbHVlcyhhcmdzKSwgYXJnc18xXzEgPSBhcmdzXzEubmV4dCgpOyAhYXJnc18xXzEuZG9uZTsgYXJnc18xXzEgPSBhcmdzXzEubmV4dCgpKSB7XG4gICAgICAgIHZhciBkYXRhID0gYXJnc18xXzEudmFsdWU7XG4gICAgICAgIHZhciBpdGVtID0gbmV3IExpc3RJdGVtKGRhdGEpO1xuICAgICAgICBpdGVtLm5leHQgPSB0aGlzLmxpc3Q7XG4gICAgICAgIGl0ZW0ucHJldiA9IHRoaXMubGlzdC5wcmV2O1xuICAgICAgICB0aGlzLmxpc3QucHJldiA9IGl0ZW07XG4gICAgICAgIGl0ZW0ucHJldi5uZXh0ID0gaXRlbTtcbiAgICAgIH1cbiAgICB9IGNhdGNoIChlXzFfMSkge1xuICAgICAgZV8xID0ge1xuICAgICAgICBlcnJvcjogZV8xXzFcbiAgICAgIH07XG4gICAgfSBmaW5hbGx5IHtcbiAgICAgIHRyeSB7XG4gICAgICAgIGlmIChhcmdzXzFfMSAmJiAhYXJnc18xXzEuZG9uZSAmJiAoX2EgPSBhcmdzXzEucmV0dXJuKSkgX2EuY2FsbChhcmdzXzEpO1xuICAgICAgfSBmaW5hbGx5IHtcbiAgICAgICAgaWYgKGVfMSkgdGhyb3cgZV8xLmVycm9yO1xuICAgICAgfVxuICAgIH1cbiAgICByZXR1cm4gdGhpcztcbiAgfTtcbiAgTGlua2VkTGlzdC5wcm90b3R5cGUucG9wID0gZnVuY3Rpb24gKCkge1xuICAgIHZhciBpdGVtID0gdGhpcy5saXN0LnByZXY7XG4gICAgaWYgKGl0ZW0uZGF0YSA9PT0gZXhwb3J0cy5FTkQpIHtcbiAgICAgIHJldHVybiBudWxsO1xuICAgIH1cbiAgICB0aGlzLmxpc3QucHJldiA9IGl0ZW0ucHJldjtcbiAgICBpdGVtLnByZXYubmV4dCA9IHRoaXMubGlzdDtcbiAgICBpdGVtLm5leHQgPSBpdGVtLnByZXYgPSBudWxsO1xuICAgIHJldHVybiBpdGVtLmRhdGE7XG4gIH07XG4gIExpbmtlZExpc3QucHJvdG90eXBlLnVuc2hpZnQgPSBmdW5jdGlvbiAoKSB7XG4gICAgdmFyIGVfMiwgX2E7XG4gICAgdmFyIGFyZ3MgPSBbXTtcbiAgICBmb3IgKHZhciBfaSA9IDA7IF9pIDwgYXJndW1lbnRzLmxlbmd0aDsgX2krKykge1xuICAgICAgYXJnc1tfaV0gPSBhcmd1bWVudHNbX2ldO1xuICAgIH1cbiAgICB0cnkge1xuICAgICAgZm9yICh2YXIgX2IgPSBfX3ZhbHVlcyhhcmdzLnNsaWNlKDApLnJldmVyc2UoKSksIF9jID0gX2IubmV4dCgpOyAhX2MuZG9uZTsgX2MgPSBfYi5uZXh0KCkpIHtcbiAgICAgICAgdmFyIGRhdGEgPSBfYy52YWx1ZTtcbiAgICAgICAgdmFyIGl0ZW0gPSBuZXcgTGlzdEl0ZW0oZGF0YSk7XG4gICAgICAgIGl0ZW0ubmV4dCA9IHRoaXMubGlzdC5uZXh0O1xuICAgICAgICBpdGVtLnByZXYgPSB0aGlzLmxpc3Q7XG4gICAgICAgIHRoaXMubGlzdC5uZXh0ID0gaXRlbTtcbiAgICAgICAgaXRlbS5uZXh0LnByZXYgPSBpdGVtO1xuICAgICAgfVxuICAgIH0gY2F0Y2ggKGVfMl8xKSB7XG4gICAgICBlXzIgPSB7XG4gICAgICAgIGVycm9yOiBlXzJfMVxuICAgICAgfTtcbiAgICB9IGZpbmFsbHkge1xuICAgICAgdHJ5IHtcbiAgICAgICAgaWYgKF9jICYmICFfYy5kb25lICYmIChfYSA9IF9iLnJldHVybikpIF9hLmNhbGwoX2IpO1xuICAgICAgfSBmaW5hbGx5IHtcbiAgICAgICAgaWYgKGVfMikgdGhyb3cgZV8yLmVycm9yO1xuICAgICAgfVxuICAgIH1cbiAgICByZXR1cm4gdGhpcztcbiAgfTtcbiAgTGlua2VkTGlzdC5wcm90b3R5cGUuc2hpZnQgPSBmdW5jdGlvbiAoKSB7XG4gICAgdmFyIGl0ZW0gPSB0aGlzLmxpc3QubmV4dDtcbiAgICBpZiAoaXRlbS5kYXRhID09PSBleHBvcnRzLkVORCkge1xuICAgICAgcmV0dXJuIG51bGw7XG4gICAgfVxuICAgIHRoaXMubGlzdC5uZXh0ID0gaXRlbS5uZXh0O1xuICAgIGl0ZW0ubmV4dC5wcmV2ID0gdGhpcy5saXN0O1xuICAgIGl0ZW0ubmV4dCA9IGl0ZW0ucHJldiA9IG51bGw7XG4gICAgcmV0dXJuIGl0ZW0uZGF0YTtcbiAgfTtcbiAgTGlua2VkTGlzdC5wcm90b3R5cGUucmVtb3ZlID0gZnVuY3Rpb24gKCkge1xuICAgIHZhciBlXzMsIF9hO1xuICAgIHZhciBpdGVtcyA9IFtdO1xuICAgIGZvciAodmFyIF9pID0gMDsgX2kgPCBhcmd1bWVudHMubGVuZ3RoOyBfaSsrKSB7XG4gICAgICBpdGVtc1tfaV0gPSBhcmd1bWVudHNbX2ldO1xuICAgIH1cbiAgICB2YXIgbWFwID0gbmV3IE1hcCgpO1xuICAgIHRyeSB7XG4gICAgICBmb3IgKHZhciBpdGVtc18xID0gX192YWx1ZXMoaXRlbXMpLCBpdGVtc18xXzEgPSBpdGVtc18xLm5leHQoKTsgIWl0ZW1zXzFfMS5kb25lOyBpdGVtc18xXzEgPSBpdGVtc18xLm5leHQoKSkge1xuICAgICAgICB2YXIgaXRlbV8xID0gaXRlbXNfMV8xLnZhbHVlO1xuICAgICAgICBtYXAuc2V0KGl0ZW1fMSwgdHJ1ZSk7XG4gICAgICB9XG4gICAgfSBjYXRjaCAoZV8zXzEpIHtcbiAgICAgIGVfMyA9IHtcbiAgICAgICAgZXJyb3I6IGVfM18xXG4gICAgICB9O1xuICAgIH0gZmluYWxseSB7XG4gICAgICB0cnkge1xuICAgICAgICBpZiAoaXRlbXNfMV8xICYmICFpdGVtc18xXzEuZG9uZSAmJiAoX2EgPSBpdGVtc18xLnJldHVybikpIF9hLmNhbGwoaXRlbXNfMSk7XG4gICAgICB9IGZpbmFsbHkge1xuICAgICAgICBpZiAoZV8zKSB0aHJvdyBlXzMuZXJyb3I7XG4gICAgICB9XG4gICAgfVxuICAgIHZhciBpdGVtID0gdGhpcy5saXN0Lm5leHQ7XG4gICAgd2hpbGUgKGl0ZW0uZGF0YSAhPT0gZXhwb3J0cy5FTkQpIHtcbiAgICAgIHZhciBuZXh0ID0gaXRlbS5uZXh0O1xuICAgICAgaWYgKG1hcC5oYXMoaXRlbS5kYXRhKSkge1xuICAgICAgICBpdGVtLnByZXYubmV4dCA9IGl0ZW0ubmV4dDtcbiAgICAgICAgaXRlbS5uZXh0LnByZXYgPSBpdGVtLnByZXY7XG4gICAgICAgIGl0ZW0ubmV4dCA9IGl0ZW0ucHJldiA9IG51bGw7XG4gICAgICB9XG4gICAgICBpdGVtID0gbmV4dDtcbiAgICB9XG4gIH07XG4gIExpbmtlZExpc3QucHJvdG90eXBlLmNsZWFyID0gZnVuY3Rpb24gKCkge1xuICAgIHRoaXMubGlzdC5uZXh0LnByZXYgPSB0aGlzLmxpc3QucHJldi5uZXh0ID0gbnVsbDtcbiAgICB0aGlzLmxpc3QubmV4dCA9IHRoaXMubGlzdC5wcmV2ID0gdGhpcy5saXN0O1xuICAgIHJldHVybiB0aGlzO1xuICB9O1xuICBMaW5rZWRMaXN0LnByb3RvdHlwZVtTeW1ib2wuaXRlcmF0b3JdID0gZnVuY3Rpb24gKCkge1xuICAgIHZhciBjdXJyZW50O1xuICAgIHJldHVybiBfX2dlbmVyYXRvcih0aGlzLCBmdW5jdGlvbiAoX2EpIHtcbiAgICAgIHN3aXRjaCAoX2EubGFiZWwpIHtcbiAgICAgICAgY2FzZSAwOlxuICAgICAgICAgIGN1cnJlbnQgPSB0aGlzLmxpc3QubmV4dDtcbiAgICAgICAgICBfYS5sYWJlbCA9IDE7XG4gICAgICAgIGNhc2UgMTpcbiAgICAgICAgICBpZiAoIShjdXJyZW50LmRhdGEgIT09IGV4cG9ydHMuRU5EKSkgcmV0dXJuIFszLCAzXTtcbiAgICAgICAgICByZXR1cm4gWzQsIGN1cnJlbnQuZGF0YV07XG4gICAgICAgIGNhc2UgMjpcbiAgICAgICAgICBfYS5zZW50KCk7XG4gICAgICAgICAgY3VycmVudCA9IGN1cnJlbnQubmV4dDtcbiAgICAgICAgICByZXR1cm4gWzMsIDFdO1xuICAgICAgICBjYXNlIDM6XG4gICAgICAgICAgcmV0dXJuIFsyXTtcbiAgICAgIH1cbiAgICB9KTtcbiAgfTtcbiAgTGlua2VkTGlzdC5wcm90b3R5cGUucmV2ZXJzZWQgPSBmdW5jdGlvbiAoKSB7XG4gICAgdmFyIGN1cnJlbnQ7XG4gICAgcmV0dXJuIF9fZ2VuZXJhdG9yKHRoaXMsIGZ1bmN0aW9uIChfYSkge1xuICAgICAgc3dpdGNoIChfYS5sYWJlbCkge1xuICAgICAgICBjYXNlIDA6XG4gICAgICAgICAgY3VycmVudCA9IHRoaXMubGlzdC5wcmV2O1xuICAgICAgICAgIF9hLmxhYmVsID0gMTtcbiAgICAgICAgY2FzZSAxOlxuICAgICAgICAgIGlmICghKGN1cnJlbnQuZGF0YSAhPT0gZXhwb3J0cy5FTkQpKSByZXR1cm4gWzMsIDNdO1xuICAgICAgICAgIHJldHVybiBbNCwgY3VycmVudC5kYXRhXTtcbiAgICAgICAgY2FzZSAyOlxuICAgICAgICAgIF9hLnNlbnQoKTtcbiAgICAgICAgICBjdXJyZW50ID0gY3VycmVudC5wcmV2O1xuICAgICAgICAgIHJldHVybiBbMywgMV07XG4gICAgICAgIGNhc2UgMzpcbiAgICAgICAgICByZXR1cm4gWzJdO1xuICAgICAgfVxuICAgIH0pO1xuICB9O1xuICBMaW5rZWRMaXN0LnByb3RvdHlwZS5pbnNlcnQgPSBmdW5jdGlvbiAoZGF0YSwgaXNCZWZvcmUpIHtcbiAgICBpZiAoaXNCZWZvcmUgPT09IHZvaWQgMCkge1xuICAgICAgaXNCZWZvcmUgPSBudWxsO1xuICAgIH1cbiAgICBpZiAoaXNCZWZvcmUgPT09IG51bGwpIHtcbiAgICAgIGlzQmVmb3JlID0gdGhpcy5pc0JlZm9yZS5iaW5kKHRoaXMpO1xuICAgIH1cbiAgICB2YXIgaXRlbSA9IG5ldyBMaXN0SXRlbShkYXRhKTtcbiAgICB2YXIgY3VyID0gdGhpcy5saXN0Lm5leHQ7XG4gICAgd2hpbGUgKGN1ci5kYXRhICE9PSBleHBvcnRzLkVORCAmJiBpc0JlZm9yZShjdXIuZGF0YSwgaXRlbS5kYXRhKSkge1xuICAgICAgY3VyID0gY3VyLm5leHQ7XG4gICAgfVxuICAgIGl0ZW0ucHJldiA9IGN1ci5wcmV2O1xuICAgIGl0ZW0ubmV4dCA9IGN1cjtcbiAgICBjdXIucHJldi5uZXh0ID0gY3VyLnByZXYgPSBpdGVtO1xuICAgIHJldHVybiB0aGlzO1xuICB9O1xuICBMaW5rZWRMaXN0LnByb3RvdHlwZS5zb3J0ID0gZnVuY3Rpb24gKGlzQmVmb3JlKSB7XG4gICAgdmFyIGVfNCwgX2E7XG4gICAgaWYgKGlzQmVmb3JlID09PSB2b2lkIDApIHtcbiAgICAgIGlzQmVmb3JlID0gbnVsbDtcbiAgICB9XG4gICAgaWYgKGlzQmVmb3JlID09PSBudWxsKSB7XG4gICAgICBpc0JlZm9yZSA9IHRoaXMuaXNCZWZvcmUuYmluZCh0aGlzKTtcbiAgICB9XG4gICAgdmFyIGxpc3RzID0gW107XG4gICAgdHJ5IHtcbiAgICAgIGZvciAodmFyIF9iID0gX192YWx1ZXModGhpcyksIF9jID0gX2IubmV4dCgpOyAhX2MuZG9uZTsgX2MgPSBfYi5uZXh0KCkpIHtcbiAgICAgICAgdmFyIGl0ZW0gPSBfYy52YWx1ZTtcbiAgICAgICAgbGlzdHMucHVzaChuZXcgTGlua2VkTGlzdChpdGVtKSk7XG4gICAgICB9XG4gICAgfSBjYXRjaCAoZV80XzEpIHtcbiAgICAgIGVfNCA9IHtcbiAgICAgICAgZXJyb3I6IGVfNF8xXG4gICAgICB9O1xuICAgIH0gZmluYWxseSB7XG4gICAgICB0cnkge1xuICAgICAgICBpZiAoX2MgJiYgIV9jLmRvbmUgJiYgKF9hID0gX2IucmV0dXJuKSkgX2EuY2FsbChfYik7XG4gICAgICB9IGZpbmFsbHkge1xuICAgICAgICBpZiAoZV80KSB0aHJvdyBlXzQuZXJyb3I7XG4gICAgICB9XG4gICAgfVxuICAgIHRoaXMubGlzdC5uZXh0ID0gdGhpcy5saXN0LnByZXYgPSB0aGlzLmxpc3Q7XG4gICAgd2hpbGUgKGxpc3RzLmxlbmd0aCA+IDEpIHtcbiAgICAgIHZhciBsMSA9IGxpc3RzLnNoaWZ0KCk7XG4gICAgICB2YXIgbDIgPSBsaXN0cy5zaGlmdCgpO1xuICAgICAgbDEubWVyZ2UobDIsIGlzQmVmb3JlKTtcbiAgICAgIGxpc3RzLnB1c2gobDEpO1xuICAgIH1cbiAgICBpZiAobGlzdHMubGVuZ3RoKSB7XG4gICAgICB0aGlzLmxpc3QgPSBsaXN0c1swXS5saXN0O1xuICAgIH1cbiAgICByZXR1cm4gdGhpcztcbiAgfTtcbiAgTGlua2VkTGlzdC5wcm90b3R5cGUubWVyZ2UgPSBmdW5jdGlvbiAobGlzdCwgaXNCZWZvcmUpIHtcbiAgICB2YXIgX2EsIF9iLCBfYywgX2QsIF9lO1xuICAgIGlmIChpc0JlZm9yZSA9PT0gdm9pZCAwKSB7XG4gICAgICBpc0JlZm9yZSA9IG51bGw7XG4gICAgfVxuICAgIGlmIChpc0JlZm9yZSA9PT0gbnVsbCkge1xuICAgICAgaXNCZWZvcmUgPSB0aGlzLmlzQmVmb3JlLmJpbmQodGhpcyk7XG4gICAgfVxuICAgIHZhciBsY3VyID0gdGhpcy5saXN0Lm5leHQ7XG4gICAgdmFyIG1jdXIgPSBsaXN0Lmxpc3QubmV4dDtcbiAgICB3aGlsZSAobGN1ci5kYXRhICE9PSBleHBvcnRzLkVORCAmJiBtY3VyLmRhdGEgIT09IGV4cG9ydHMuRU5EKSB7XG4gICAgICBpZiAoaXNCZWZvcmUobWN1ci5kYXRhLCBsY3VyLmRhdGEpKSB7XG4gICAgICAgIF9hID0gX19yZWFkKFtsY3VyLCBtY3VyXSwgMiksIG1jdXIucHJldi5uZXh0ID0gX2FbMF0sIGxjdXIucHJldi5uZXh0ID0gX2FbMV07XG4gICAgICAgIF9iID0gX19yZWFkKFtsY3VyLnByZXYsIG1jdXIucHJldl0sIDIpLCBtY3VyLnByZXYgPSBfYlswXSwgbGN1ci5wcmV2ID0gX2JbMV07XG4gICAgICAgIF9jID0gX19yZWFkKFtsaXN0Lmxpc3QsIHRoaXMubGlzdF0sIDIpLCB0aGlzLmxpc3QucHJldi5uZXh0ID0gX2NbMF0sIGxpc3QubGlzdC5wcmV2Lm5leHQgPSBfY1sxXTtcbiAgICAgICAgX2QgPSBfX3JlYWQoW2xpc3QubGlzdC5wcmV2LCB0aGlzLmxpc3QucHJldl0sIDIpLCB0aGlzLmxpc3QucHJldiA9IF9kWzBdLCBsaXN0Lmxpc3QucHJldiA9IF9kWzFdO1xuICAgICAgICBfZSA9IF9fcmVhZChbbWN1ci5uZXh0LCBsY3VyXSwgMiksIGxjdXIgPSBfZVswXSwgbWN1ciA9IF9lWzFdO1xuICAgICAgfSBlbHNlIHtcbiAgICAgICAgbGN1ciA9IGxjdXIubmV4dDtcbiAgICAgIH1cbiAgICB9XG4gICAgaWYgKG1jdXIuZGF0YSAhPT0gZXhwb3J0cy5FTkQpIHtcbiAgICAgIHRoaXMubGlzdC5wcmV2Lm5leHQgPSBsaXN0Lmxpc3QubmV4dDtcbiAgICAgIGxpc3QubGlzdC5uZXh0LnByZXYgPSB0aGlzLmxpc3QucHJldjtcbiAgICAgIGxpc3QubGlzdC5wcmV2Lm5leHQgPSB0aGlzLmxpc3Q7XG4gICAgICB0aGlzLmxpc3QucHJldiA9IGxpc3QubGlzdC5wcmV2O1xuICAgICAgbGlzdC5saXN0Lm5leHQgPSBsaXN0Lmxpc3QucHJldiA9IGxpc3QubGlzdDtcbiAgICB9XG4gICAgcmV0dXJuIHRoaXM7XG4gIH07XG4gIHJldHVybiBMaW5rZWRMaXN0O1xufSgpO1xuZXhwb3J0cy5MaW5rZWRMaXN0ID0gTGlua2VkTGlzdDsiLCJcInVzZSBzdHJpY3RcIjtcblxuT2JqZWN0LmRlZmluZVByb3BlcnR5KGV4cG9ydHMsIFwiX19lc01vZHVsZVwiLCB7XG4gIHZhbHVlOiB0cnVlXG59KTtcbmV4cG9ydHMuUHJpb3JpdGl6ZWRMaXN0ID0gdm9pZCAwO1xudmFyIFByaW9yaXRpemVkTGlzdCA9IGZ1bmN0aW9uICgpIHtcbiAgZnVuY3Rpb24gUHJpb3JpdGl6ZWRMaXN0KCkge1xuICAgIHRoaXMuaXRlbXMgPSBbXTtcbiAgICB0aGlzLml0ZW1zID0gW107XG4gIH1cbiAgUHJpb3JpdGl6ZWRMaXN0LnByb3RvdHlwZVtTeW1ib2wuaXRlcmF0b3JdID0gZnVuY3Rpb24gKCkge1xuICAgIHZhciBpID0gMDtcbiAgICB2YXIgaXRlbXMgPSB0aGlzLml0ZW1zO1xuICAgIHJldHVybiB7XG4gICAgICBuZXh0OiBmdW5jdGlvbiAoKSB7XG4gICAgICAgIHJldHVybiB7XG4gICAgICAgICAgdmFsdWU6IGl0ZW1zW2krK10sXG4gICAgICAgICAgZG9uZTogaSA+IGl0ZW1zLmxlbmd0aFxuICAgICAgICB9O1xuICAgICAgfVxuICAgIH07XG4gIH07XG4gIFByaW9yaXRpemVkTGlzdC5wcm90b3R5cGUuYWRkID0gZnVuY3Rpb24gKGl0ZW0sIHByaW9yaXR5KSB7XG4gICAgaWYgKHByaW9yaXR5ID09PSB2b2lkIDApIHtcbiAgICAgIHByaW9yaXR5ID0gUHJpb3JpdGl6ZWRMaXN0LkRFRkFVTFRQUklPUklUWTtcbiAgICB9XG4gICAgdmFyIGkgPSB0aGlzLml0ZW1zLmxlbmd0aDtcbiAgICBkbyB7XG4gICAgICBpLS07XG4gICAgfSB3aGlsZSAoaSA+PSAwICYmIHByaW9yaXR5IDwgdGhpcy5pdGVtc1tpXS5wcmlvcml0eSk7XG4gICAgdGhpcy5pdGVtcy5zcGxpY2UoaSArIDEsIDAsIHtcbiAgICAgIGl0ZW06IGl0ZW0sXG4gICAgICBwcmlvcml0eTogcHJpb3JpdHlcbiAgICB9KTtcbiAgICByZXR1cm4gaXRlbTtcbiAgfTtcbiAgUHJpb3JpdGl6ZWRMaXN0LnByb3RvdHlwZS5yZW1vdmUgPSBmdW5jdGlvbiAoaXRlbSkge1xuICAgIHZhciBpID0gdGhpcy5pdGVtcy5sZW5ndGg7XG4gICAgZG8ge1xuICAgICAgaS0tO1xuICAgIH0gd2hpbGUgKGkgPj0gMCAmJiB0aGlzLml0ZW1zW2ldLml0ZW0gIT09IGl0ZW0pO1xuICAgIGlmIChpID49IDApIHtcbiAgICAgIHRoaXMuaXRlbXMuc3BsaWNlKGksIDEpO1xuICAgIH1cbiAgfTtcbiAgUHJpb3JpdGl6ZWRMaXN0LkRFRkFVTFRQUklPUklUWSA9IDU7XG4gIHJldHVybiBQcmlvcml0aXplZExpc3Q7XG59KCk7XG5leHBvcnRzLlByaW9yaXRpemVkTGlzdCA9IFByaW9yaXRpemVkTGlzdDsiXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=
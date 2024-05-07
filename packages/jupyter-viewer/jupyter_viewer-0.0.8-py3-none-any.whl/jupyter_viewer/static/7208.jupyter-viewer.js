"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[7208],{

/***/ 55635:
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {



var _a;
Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports.MML = void 0;
var MmlNode_js_1 = __webpack_require__(34690);
var math_js_1 = __webpack_require__(45710);
var mi_js_1 = __webpack_require__(18000);
var mn_js_1 = __webpack_require__(15600);
var mo_js_1 = __webpack_require__(77455);
var mtext_js_1 = __webpack_require__(48737);
var mspace_js_1 = __webpack_require__(43501);
var ms_js_1 = __webpack_require__(95444);
var mrow_js_1 = __webpack_require__(82139);
var mfrac_js_1 = __webpack_require__(32331);
var msqrt_js_1 = __webpack_require__(73132);
var mroot_js_1 = __webpack_require__(67465);
var mstyle_js_1 = __webpack_require__(52229);
var merror_js_1 = __webpack_require__(32808);
var mpadded_js_1 = __webpack_require__(87634);
var mphantom_js_1 = __webpack_require__(33831);
var mfenced_js_1 = __webpack_require__(54914);
var menclose_js_1 = __webpack_require__(3447);
var maction_js_1 = __webpack_require__(87968);
var msubsup_js_1 = __webpack_require__(50978);
var munderover_js_1 = __webpack_require__(42937);
var mmultiscripts_js_1 = __webpack_require__(36500);
var mtable_js_1 = __webpack_require__(32853);
var mtr_js_1 = __webpack_require__(8610);
var mtd_js_1 = __webpack_require__(1887);
var maligngroup_js_1 = __webpack_require__(48856);
var malignmark_js_1 = __webpack_require__(71005);
var mglyph_js_1 = __webpack_require__(80465);
var semantics_js_1 = __webpack_require__(44924);
var TeXAtom_js_1 = __webpack_require__(57661);
var mathchoice_js_1 = __webpack_require__(81498);
exports.MML = (_a = {}, _a[math_js_1.MmlMath.prototype.kind] = math_js_1.MmlMath, _a[mi_js_1.MmlMi.prototype.kind] = mi_js_1.MmlMi, _a[mn_js_1.MmlMn.prototype.kind] = mn_js_1.MmlMn, _a[mo_js_1.MmlMo.prototype.kind] = mo_js_1.MmlMo, _a[mtext_js_1.MmlMtext.prototype.kind] = mtext_js_1.MmlMtext, _a[mspace_js_1.MmlMspace.prototype.kind] = mspace_js_1.MmlMspace, _a[ms_js_1.MmlMs.prototype.kind] = ms_js_1.MmlMs, _a[mrow_js_1.MmlMrow.prototype.kind] = mrow_js_1.MmlMrow, _a[mrow_js_1.MmlInferredMrow.prototype.kind] = mrow_js_1.MmlInferredMrow, _a[mfrac_js_1.MmlMfrac.prototype.kind] = mfrac_js_1.MmlMfrac, _a[msqrt_js_1.MmlMsqrt.prototype.kind] = msqrt_js_1.MmlMsqrt, _a[mroot_js_1.MmlMroot.prototype.kind] = mroot_js_1.MmlMroot, _a[mstyle_js_1.MmlMstyle.prototype.kind] = mstyle_js_1.MmlMstyle, _a[merror_js_1.MmlMerror.prototype.kind] = merror_js_1.MmlMerror, _a[mpadded_js_1.MmlMpadded.prototype.kind] = mpadded_js_1.MmlMpadded, _a[mphantom_js_1.MmlMphantom.prototype.kind] = mphantom_js_1.MmlMphantom, _a[mfenced_js_1.MmlMfenced.prototype.kind] = mfenced_js_1.MmlMfenced, _a[menclose_js_1.MmlMenclose.prototype.kind] = menclose_js_1.MmlMenclose, _a[maction_js_1.MmlMaction.prototype.kind] = maction_js_1.MmlMaction, _a[msubsup_js_1.MmlMsub.prototype.kind] = msubsup_js_1.MmlMsub, _a[msubsup_js_1.MmlMsup.prototype.kind] = msubsup_js_1.MmlMsup, _a[msubsup_js_1.MmlMsubsup.prototype.kind] = msubsup_js_1.MmlMsubsup, _a[munderover_js_1.MmlMunder.prototype.kind] = munderover_js_1.MmlMunder, _a[munderover_js_1.MmlMover.prototype.kind] = munderover_js_1.MmlMover, _a[munderover_js_1.MmlMunderover.prototype.kind] = munderover_js_1.MmlMunderover, _a[mmultiscripts_js_1.MmlMmultiscripts.prototype.kind] = mmultiscripts_js_1.MmlMmultiscripts, _a[mmultiscripts_js_1.MmlMprescripts.prototype.kind] = mmultiscripts_js_1.MmlMprescripts, _a[mmultiscripts_js_1.MmlNone.prototype.kind] = mmultiscripts_js_1.MmlNone, _a[mtable_js_1.MmlMtable.prototype.kind] = mtable_js_1.MmlMtable, _a[mtr_js_1.MmlMlabeledtr.prototype.kind] = mtr_js_1.MmlMlabeledtr, _a[mtr_js_1.MmlMtr.prototype.kind] = mtr_js_1.MmlMtr, _a[mtd_js_1.MmlMtd.prototype.kind] = mtd_js_1.MmlMtd, _a[maligngroup_js_1.MmlMaligngroup.prototype.kind] = maligngroup_js_1.MmlMaligngroup, _a[malignmark_js_1.MmlMalignmark.prototype.kind] = malignmark_js_1.MmlMalignmark, _a[mglyph_js_1.MmlMglyph.prototype.kind] = mglyph_js_1.MmlMglyph, _a[semantics_js_1.MmlSemantics.prototype.kind] = semantics_js_1.MmlSemantics, _a[semantics_js_1.MmlAnnotation.prototype.kind] = semantics_js_1.MmlAnnotation, _a[semantics_js_1.MmlAnnotationXML.prototype.kind] = semantics_js_1.MmlAnnotationXML, _a[TeXAtom_js_1.TeXAtom.prototype.kind] = TeXAtom_js_1.TeXAtom, _a[mathchoice_js_1.MathChoice.prototype.kind] = mathchoice_js_1.MathChoice, _a[MmlNode_js_1.TextNode.prototype.kind] = MmlNode_js_1.TextNode, _a[MmlNode_js_1.XMLNode.prototype.kind] = MmlNode_js_1.XMLNode, _a);

/***/ }),

/***/ 77208:
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
exports.MmlFactory = void 0;
var NodeFactory_js_1 = __webpack_require__(93366);
var MML_js_1 = __webpack_require__(55635);
var MmlFactory = function (_super) {
  __extends(MmlFactory, _super);
  function MmlFactory() {
    return _super !== null && _super.apply(this, arguments) || this;
  }
  Object.defineProperty(MmlFactory.prototype, "MML", {
    get: function () {
      return this.node;
    },
    enumerable: false,
    configurable: true
  });
  MmlFactory.defaultNodes = MML_js_1.MML;
  return MmlFactory;
}(NodeFactory_js_1.AbstractNodeFactory);
exports.MmlFactory = MmlFactory;

/***/ }),

/***/ 48856:
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
Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports.MmlMaligngroup = void 0;
var MmlNode_js_1 = __webpack_require__(34690);
var Attributes_js_1 = __webpack_require__(39930);
var MmlMaligngroup = function (_super) {
  __extends(MmlMaligngroup, _super);
  function MmlMaligngroup() {
    return _super !== null && _super.apply(this, arguments) || this;
  }
  Object.defineProperty(MmlMaligngroup.prototype, "kind", {
    get: function () {
      return 'maligngroup';
    },
    enumerable: false,
    configurable: true
  });
  Object.defineProperty(MmlMaligngroup.prototype, "isSpacelike", {
    get: function () {
      return true;
    },
    enumerable: false,
    configurable: true
  });
  MmlMaligngroup.prototype.setChildInheritedAttributes = function (attributes, display, level, prime) {
    attributes = this.addInheritedAttributes(attributes, this.attributes.getAllAttributes());
    _super.prototype.setChildInheritedAttributes.call(this, attributes, display, level, prime);
  };
  MmlMaligngroup.defaults = __assign(__assign({}, MmlNode_js_1.AbstractMmlLayoutNode.defaults), {
    groupalign: Attributes_js_1.INHERIT
  });
  return MmlMaligngroup;
}(MmlNode_js_1.AbstractMmlLayoutNode);
exports.MmlMaligngroup = MmlMaligngroup;

/***/ }),

/***/ 71005:
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
Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports.MmlMalignmark = void 0;
var MmlNode_js_1 = __webpack_require__(34690);
var MmlMalignmark = function (_super) {
  __extends(MmlMalignmark, _super);
  function MmlMalignmark() {
    return _super !== null && _super.apply(this, arguments) || this;
  }
  Object.defineProperty(MmlMalignmark.prototype, "kind", {
    get: function () {
      return 'malignmark';
    },
    enumerable: false,
    configurable: true
  });
  Object.defineProperty(MmlMalignmark.prototype, "arity", {
    get: function () {
      return 0;
    },
    enumerable: false,
    configurable: true
  });
  Object.defineProperty(MmlMalignmark.prototype, "isSpacelike", {
    get: function () {
      return true;
    },
    enumerable: false,
    configurable: true
  });
  MmlMalignmark.defaults = __assign(__assign({}, MmlNode_js_1.AbstractMmlNode.defaults), {
    edge: 'left'
  });
  return MmlMalignmark;
}(MmlNode_js_1.AbstractMmlNode);
exports.MmlMalignmark = MmlMalignmark;

/***/ }),

/***/ 81498:
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
Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports.MathChoice = void 0;
var MmlNode_js_1 = __webpack_require__(34690);
var MathChoice = function (_super) {
  __extends(MathChoice, _super);
  function MathChoice() {
    return _super !== null && _super.apply(this, arguments) || this;
  }
  Object.defineProperty(MathChoice.prototype, "kind", {
    get: function () {
      return 'MathChoice';
    },
    enumerable: false,
    configurable: true
  });
  Object.defineProperty(MathChoice.prototype, "arity", {
    get: function () {
      return 4;
    },
    enumerable: false,
    configurable: true
  });
  Object.defineProperty(MathChoice.prototype, "notParent", {
    get: function () {
      return true;
    },
    enumerable: false,
    configurable: true
  });
  MathChoice.prototype.setInheritedAttributes = function (attributes, display, level, prime) {
    var selection = display ? 0 : Math.max(0, Math.min(level, 2)) + 1;
    var child = this.childNodes[selection] || this.factory.create('mrow');
    this.parent.replaceChild(child, this);
    child.setInheritedAttributes(attributes, display, level, prime);
  };
  MathChoice.defaults = __assign({}, MmlNode_js_1.AbstractMmlBaseNode.defaults);
  return MathChoice;
}(MmlNode_js_1.AbstractMmlBaseNode);
exports.MathChoice = MathChoice;

/***/ }),

/***/ 32808:
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
Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports.MmlMerror = void 0;
var MmlNode_js_1 = __webpack_require__(34690);
var MmlMerror = function (_super) {
  __extends(MmlMerror, _super);
  function MmlMerror() {
    var _this = _super !== null && _super.apply(this, arguments) || this;
    _this.texclass = MmlNode_js_1.TEXCLASS.ORD;
    return _this;
  }
  Object.defineProperty(MmlMerror.prototype, "kind", {
    get: function () {
      return 'merror';
    },
    enumerable: false,
    configurable: true
  });
  Object.defineProperty(MmlMerror.prototype, "arity", {
    get: function () {
      return -1;
    },
    enumerable: false,
    configurable: true
  });
  Object.defineProperty(MmlMerror.prototype, "linebreakContainer", {
    get: function () {
      return true;
    },
    enumerable: false,
    configurable: true
  });
  MmlMerror.defaults = __assign({}, MmlNode_js_1.AbstractMmlNode.defaults);
  return MmlMerror;
}(MmlNode_js_1.AbstractMmlNode);
exports.MmlMerror = MmlMerror;

/***/ }),

/***/ 33831:
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
Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports.MmlMphantom = void 0;
var MmlNode_js_1 = __webpack_require__(34690);
var MmlMphantom = function (_super) {
  __extends(MmlMphantom, _super);
  function MmlMphantom() {
    var _this = _super !== null && _super.apply(this, arguments) || this;
    _this.texclass = MmlNode_js_1.TEXCLASS.ORD;
    return _this;
  }
  Object.defineProperty(MmlMphantom.prototype, "kind", {
    get: function () {
      return 'mphantom';
    },
    enumerable: false,
    configurable: true
  });
  MmlMphantom.defaults = __assign({}, MmlNode_js_1.AbstractMmlLayoutNode.defaults);
  return MmlMphantom;
}(MmlNode_js_1.AbstractMmlLayoutNode);
exports.MmlMphantom = MmlMphantom;

/***/ }),

/***/ 52229:
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
Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports.MmlMstyle = void 0;
var MmlNode_js_1 = __webpack_require__(34690);
var Attributes_js_1 = __webpack_require__(39930);
var MmlMstyle = function (_super) {
  __extends(MmlMstyle, _super);
  function MmlMstyle() {
    return _super !== null && _super.apply(this, arguments) || this;
  }
  Object.defineProperty(MmlMstyle.prototype, "kind", {
    get: function () {
      return 'mstyle';
    },
    enumerable: false,
    configurable: true
  });
  Object.defineProperty(MmlMstyle.prototype, "notParent", {
    get: function () {
      return this.childNodes[0] && this.childNodes[0].childNodes.length === 1;
    },
    enumerable: false,
    configurable: true
  });
  MmlMstyle.prototype.setChildInheritedAttributes = function (attributes, display, level, prime) {
    var scriptlevel = this.attributes.getExplicit('scriptlevel');
    if (scriptlevel != null) {
      scriptlevel = scriptlevel.toString();
      if (scriptlevel.match(/^\s*[-+]/)) {
        level += parseInt(scriptlevel);
      } else {
        level = parseInt(scriptlevel);
      }
      prime = false;
    }
    var displaystyle = this.attributes.getExplicit('displaystyle');
    if (displaystyle != null) {
      display = displaystyle === true;
      prime = false;
    }
    var cramped = this.attributes.getExplicit('data-cramped');
    if (cramped != null) {
      prime = cramped;
    }
    attributes = this.addInheritedAttributes(attributes, this.attributes.getAllAttributes());
    this.childNodes[0].setInheritedAttributes(attributes, display, level, prime);
  };
  MmlMstyle.defaults = __assign(__assign({}, MmlNode_js_1.AbstractMmlLayoutNode.defaults), {
    scriptlevel: Attributes_js_1.INHERIT,
    displaystyle: Attributes_js_1.INHERIT,
    scriptsizemultiplier: 1 / Math.sqrt(2),
    scriptminsize: '8px',
    mathbackground: Attributes_js_1.INHERIT,
    mathcolor: Attributes_js_1.INHERIT,
    dir: Attributes_js_1.INHERIT,
    infixlinebreakstyle: 'before'
  });
  return MmlMstyle;
}(MmlNode_js_1.AbstractMmlLayoutNode);
exports.MmlMstyle = MmlMstyle;

/***/ }),

/***/ 93366:
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
exports.AbstractNodeFactory = void 0;
var Factory_js_1 = __webpack_require__(26445);
var AbstractNodeFactory = function (_super) {
  __extends(AbstractNodeFactory, _super);
  function AbstractNodeFactory() {
    return _super !== null && _super.apply(this, arguments) || this;
  }
  AbstractNodeFactory.prototype.create = function (kind, properties, children) {
    if (properties === void 0) {
      properties = {};
    }
    if (children === void 0) {
      children = [];
    }
    return this.node[kind](properties, children);
  };
  return AbstractNodeFactory;
}(Factory_js_1.AbstractFactory);
exports.AbstractNodeFactory = AbstractNodeFactory;

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiNzIwOC5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7QUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7Ozs7Ozs7QUN0Q0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7Ozs7OztBQzNDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7Ozs7OztBQ2xFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7Ozs7Ozs7QUNwRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7Ozs7Ozs7QUN4RUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOzs7Ozs7O0FDcEVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOzs7Ozs7O0FDdERBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7Ozs7OztBQzVGQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vQGRhdGFsYXllci9qdXB5dGVyLXZpZXdlci8uL25vZGVfbW9kdWxlcy9tYXRoamF4LWZ1bGwvanMvY29yZS9NbWxUcmVlL01NTC5qcyIsIndlYnBhY2s6Ly9AZGF0YWxheWVyL2p1cHl0ZXItdmlld2VyLy4vbm9kZV9tb2R1bGVzL21hdGhqYXgtZnVsbC9qcy9jb3JlL01tbFRyZWUvTW1sRmFjdG9yeS5qcyIsIndlYnBhY2s6Ly9AZGF0YWxheWVyL2p1cHl0ZXItdmlld2VyLy4vbm9kZV9tb2R1bGVzL21hdGhqYXgtZnVsbC9qcy9jb3JlL01tbFRyZWUvTW1sTm9kZXMvbWFsaWduZ3JvdXAuanMiLCJ3ZWJwYWNrOi8vQGRhdGFsYXllci9qdXB5dGVyLXZpZXdlci8uL25vZGVfbW9kdWxlcy9tYXRoamF4LWZ1bGwvanMvY29yZS9NbWxUcmVlL01tbE5vZGVzL21hbGlnbm1hcmsuanMiLCJ3ZWJwYWNrOi8vQGRhdGFsYXllci9qdXB5dGVyLXZpZXdlci8uL25vZGVfbW9kdWxlcy9tYXRoamF4LWZ1bGwvanMvY29yZS9NbWxUcmVlL01tbE5vZGVzL21hdGhjaG9pY2UuanMiLCJ3ZWJwYWNrOi8vQGRhdGFsYXllci9qdXB5dGVyLXZpZXdlci8uL25vZGVfbW9kdWxlcy9tYXRoamF4LWZ1bGwvanMvY29yZS9NbWxUcmVlL01tbE5vZGVzL21lcnJvci5qcyIsIndlYnBhY2s6Ly9AZGF0YWxheWVyL2p1cHl0ZXItdmlld2VyLy4vbm9kZV9tb2R1bGVzL21hdGhqYXgtZnVsbC9qcy9jb3JlL01tbFRyZWUvTW1sTm9kZXMvbXBoYW50b20uanMiLCJ3ZWJwYWNrOi8vQGRhdGFsYXllci9qdXB5dGVyLXZpZXdlci8uL25vZGVfbW9kdWxlcy9tYXRoamF4LWZ1bGwvanMvY29yZS9NbWxUcmVlL01tbE5vZGVzL21zdHlsZS5qcyIsIndlYnBhY2s6Ly9AZGF0YWxheWVyL2p1cHl0ZXItdmlld2VyLy4vbm9kZV9tb2R1bGVzL21hdGhqYXgtZnVsbC9qcy9jb3JlL1RyZWUvTm9kZUZhY3RvcnkuanMiXSwic291cmNlc0NvbnRlbnQiOlsiXCJ1c2Ugc3RyaWN0XCI7XG5cbnZhciBfYTtcbk9iamVjdC5kZWZpbmVQcm9wZXJ0eShleHBvcnRzLCBcIl9fZXNNb2R1bGVcIiwge1xuICB2YWx1ZTogdHJ1ZVxufSk7XG5leHBvcnRzLk1NTCA9IHZvaWQgMDtcbnZhciBNbWxOb2RlX2pzXzEgPSByZXF1aXJlKFwiLi9NbWxOb2RlLmpzXCIpO1xudmFyIG1hdGhfanNfMSA9IHJlcXVpcmUoXCIuL01tbE5vZGVzL21hdGguanNcIik7XG52YXIgbWlfanNfMSA9IHJlcXVpcmUoXCIuL01tbE5vZGVzL21pLmpzXCIpO1xudmFyIG1uX2pzXzEgPSByZXF1aXJlKFwiLi9NbWxOb2Rlcy9tbi5qc1wiKTtcbnZhciBtb19qc18xID0gcmVxdWlyZShcIi4vTW1sTm9kZXMvbW8uanNcIik7XG52YXIgbXRleHRfanNfMSA9IHJlcXVpcmUoXCIuL01tbE5vZGVzL210ZXh0LmpzXCIpO1xudmFyIG1zcGFjZV9qc18xID0gcmVxdWlyZShcIi4vTW1sTm9kZXMvbXNwYWNlLmpzXCIpO1xudmFyIG1zX2pzXzEgPSByZXF1aXJlKFwiLi9NbWxOb2Rlcy9tcy5qc1wiKTtcbnZhciBtcm93X2pzXzEgPSByZXF1aXJlKFwiLi9NbWxOb2Rlcy9tcm93LmpzXCIpO1xudmFyIG1mcmFjX2pzXzEgPSByZXF1aXJlKFwiLi9NbWxOb2Rlcy9tZnJhYy5qc1wiKTtcbnZhciBtc3FydF9qc18xID0gcmVxdWlyZShcIi4vTW1sTm9kZXMvbXNxcnQuanNcIik7XG52YXIgbXJvb3RfanNfMSA9IHJlcXVpcmUoXCIuL01tbE5vZGVzL21yb290LmpzXCIpO1xudmFyIG1zdHlsZV9qc18xID0gcmVxdWlyZShcIi4vTW1sTm9kZXMvbXN0eWxlLmpzXCIpO1xudmFyIG1lcnJvcl9qc18xID0gcmVxdWlyZShcIi4vTW1sTm9kZXMvbWVycm9yLmpzXCIpO1xudmFyIG1wYWRkZWRfanNfMSA9IHJlcXVpcmUoXCIuL01tbE5vZGVzL21wYWRkZWQuanNcIik7XG52YXIgbXBoYW50b21fanNfMSA9IHJlcXVpcmUoXCIuL01tbE5vZGVzL21waGFudG9tLmpzXCIpO1xudmFyIG1mZW5jZWRfanNfMSA9IHJlcXVpcmUoXCIuL01tbE5vZGVzL21mZW5jZWQuanNcIik7XG52YXIgbWVuY2xvc2VfanNfMSA9IHJlcXVpcmUoXCIuL01tbE5vZGVzL21lbmNsb3NlLmpzXCIpO1xudmFyIG1hY3Rpb25fanNfMSA9IHJlcXVpcmUoXCIuL01tbE5vZGVzL21hY3Rpb24uanNcIik7XG52YXIgbXN1YnN1cF9qc18xID0gcmVxdWlyZShcIi4vTW1sTm9kZXMvbXN1YnN1cC5qc1wiKTtcbnZhciBtdW5kZXJvdmVyX2pzXzEgPSByZXF1aXJlKFwiLi9NbWxOb2Rlcy9tdW5kZXJvdmVyLmpzXCIpO1xudmFyIG1tdWx0aXNjcmlwdHNfanNfMSA9IHJlcXVpcmUoXCIuL01tbE5vZGVzL21tdWx0aXNjcmlwdHMuanNcIik7XG52YXIgbXRhYmxlX2pzXzEgPSByZXF1aXJlKFwiLi9NbWxOb2Rlcy9tdGFibGUuanNcIik7XG52YXIgbXRyX2pzXzEgPSByZXF1aXJlKFwiLi9NbWxOb2Rlcy9tdHIuanNcIik7XG52YXIgbXRkX2pzXzEgPSByZXF1aXJlKFwiLi9NbWxOb2Rlcy9tdGQuanNcIik7XG52YXIgbWFsaWduZ3JvdXBfanNfMSA9IHJlcXVpcmUoXCIuL01tbE5vZGVzL21hbGlnbmdyb3VwLmpzXCIpO1xudmFyIG1hbGlnbm1hcmtfanNfMSA9IHJlcXVpcmUoXCIuL01tbE5vZGVzL21hbGlnbm1hcmsuanNcIik7XG52YXIgbWdseXBoX2pzXzEgPSByZXF1aXJlKFwiLi9NbWxOb2Rlcy9tZ2x5cGguanNcIik7XG52YXIgc2VtYW50aWNzX2pzXzEgPSByZXF1aXJlKFwiLi9NbWxOb2Rlcy9zZW1hbnRpY3MuanNcIik7XG52YXIgVGVYQXRvbV9qc18xID0gcmVxdWlyZShcIi4vTW1sTm9kZXMvVGVYQXRvbS5qc1wiKTtcbnZhciBtYXRoY2hvaWNlX2pzXzEgPSByZXF1aXJlKFwiLi9NbWxOb2Rlcy9tYXRoY2hvaWNlLmpzXCIpO1xuZXhwb3J0cy5NTUwgPSAoX2EgPSB7fSwgX2FbbWF0aF9qc18xLk1tbE1hdGgucHJvdG90eXBlLmtpbmRdID0gbWF0aF9qc18xLk1tbE1hdGgsIF9hW21pX2pzXzEuTW1sTWkucHJvdG90eXBlLmtpbmRdID0gbWlfanNfMS5NbWxNaSwgX2FbbW5fanNfMS5NbWxNbi5wcm90b3R5cGUua2luZF0gPSBtbl9qc18xLk1tbE1uLCBfYVttb19qc18xLk1tbE1vLnByb3RvdHlwZS5raW5kXSA9IG1vX2pzXzEuTW1sTW8sIF9hW210ZXh0X2pzXzEuTW1sTXRleHQucHJvdG90eXBlLmtpbmRdID0gbXRleHRfanNfMS5NbWxNdGV4dCwgX2FbbXNwYWNlX2pzXzEuTW1sTXNwYWNlLnByb3RvdHlwZS5raW5kXSA9IG1zcGFjZV9qc18xLk1tbE1zcGFjZSwgX2FbbXNfanNfMS5NbWxNcy5wcm90b3R5cGUua2luZF0gPSBtc19qc18xLk1tbE1zLCBfYVttcm93X2pzXzEuTW1sTXJvdy5wcm90b3R5cGUua2luZF0gPSBtcm93X2pzXzEuTW1sTXJvdywgX2FbbXJvd19qc18xLk1tbEluZmVycmVkTXJvdy5wcm90b3R5cGUua2luZF0gPSBtcm93X2pzXzEuTW1sSW5mZXJyZWRNcm93LCBfYVttZnJhY19qc18xLk1tbE1mcmFjLnByb3RvdHlwZS5raW5kXSA9IG1mcmFjX2pzXzEuTW1sTWZyYWMsIF9hW21zcXJ0X2pzXzEuTW1sTXNxcnQucHJvdG90eXBlLmtpbmRdID0gbXNxcnRfanNfMS5NbWxNc3FydCwgX2FbbXJvb3RfanNfMS5NbWxNcm9vdC5wcm90b3R5cGUua2luZF0gPSBtcm9vdF9qc18xLk1tbE1yb290LCBfYVttc3R5bGVfanNfMS5NbWxNc3R5bGUucHJvdG90eXBlLmtpbmRdID0gbXN0eWxlX2pzXzEuTW1sTXN0eWxlLCBfYVttZXJyb3JfanNfMS5NbWxNZXJyb3IucHJvdG90eXBlLmtpbmRdID0gbWVycm9yX2pzXzEuTW1sTWVycm9yLCBfYVttcGFkZGVkX2pzXzEuTW1sTXBhZGRlZC5wcm90b3R5cGUua2luZF0gPSBtcGFkZGVkX2pzXzEuTW1sTXBhZGRlZCwgX2FbbXBoYW50b21fanNfMS5NbWxNcGhhbnRvbS5wcm90b3R5cGUua2luZF0gPSBtcGhhbnRvbV9qc18xLk1tbE1waGFudG9tLCBfYVttZmVuY2VkX2pzXzEuTW1sTWZlbmNlZC5wcm90b3R5cGUua2luZF0gPSBtZmVuY2VkX2pzXzEuTW1sTWZlbmNlZCwgX2FbbWVuY2xvc2VfanNfMS5NbWxNZW5jbG9zZS5wcm90b3R5cGUua2luZF0gPSBtZW5jbG9zZV9qc18xLk1tbE1lbmNsb3NlLCBfYVttYWN0aW9uX2pzXzEuTW1sTWFjdGlvbi5wcm90b3R5cGUua2luZF0gPSBtYWN0aW9uX2pzXzEuTW1sTWFjdGlvbiwgX2FbbXN1YnN1cF9qc18xLk1tbE1zdWIucHJvdG90eXBlLmtpbmRdID0gbXN1YnN1cF9qc18xLk1tbE1zdWIsIF9hW21zdWJzdXBfanNfMS5NbWxNc3VwLnByb3RvdHlwZS5raW5kXSA9IG1zdWJzdXBfanNfMS5NbWxNc3VwLCBfYVttc3Vic3VwX2pzXzEuTW1sTXN1YnN1cC5wcm90b3R5cGUua2luZF0gPSBtc3Vic3VwX2pzXzEuTW1sTXN1YnN1cCwgX2FbbXVuZGVyb3Zlcl9qc18xLk1tbE11bmRlci5wcm90b3R5cGUua2luZF0gPSBtdW5kZXJvdmVyX2pzXzEuTW1sTXVuZGVyLCBfYVttdW5kZXJvdmVyX2pzXzEuTW1sTW92ZXIucHJvdG90eXBlLmtpbmRdID0gbXVuZGVyb3Zlcl9qc18xLk1tbE1vdmVyLCBfYVttdW5kZXJvdmVyX2pzXzEuTW1sTXVuZGVyb3Zlci5wcm90b3R5cGUua2luZF0gPSBtdW5kZXJvdmVyX2pzXzEuTW1sTXVuZGVyb3ZlciwgX2FbbW11bHRpc2NyaXB0c19qc18xLk1tbE1tdWx0aXNjcmlwdHMucHJvdG90eXBlLmtpbmRdID0gbW11bHRpc2NyaXB0c19qc18xLk1tbE1tdWx0aXNjcmlwdHMsIF9hW21tdWx0aXNjcmlwdHNfanNfMS5NbWxNcHJlc2NyaXB0cy5wcm90b3R5cGUua2luZF0gPSBtbXVsdGlzY3JpcHRzX2pzXzEuTW1sTXByZXNjcmlwdHMsIF9hW21tdWx0aXNjcmlwdHNfanNfMS5NbWxOb25lLnByb3RvdHlwZS5raW5kXSA9IG1tdWx0aXNjcmlwdHNfanNfMS5NbWxOb25lLCBfYVttdGFibGVfanNfMS5NbWxNdGFibGUucHJvdG90eXBlLmtpbmRdID0gbXRhYmxlX2pzXzEuTW1sTXRhYmxlLCBfYVttdHJfanNfMS5NbWxNbGFiZWxlZHRyLnByb3RvdHlwZS5raW5kXSA9IG10cl9qc18xLk1tbE1sYWJlbGVkdHIsIF9hW210cl9qc18xLk1tbE10ci5wcm90b3R5cGUua2luZF0gPSBtdHJfanNfMS5NbWxNdHIsIF9hW210ZF9qc18xLk1tbE10ZC5wcm90b3R5cGUua2luZF0gPSBtdGRfanNfMS5NbWxNdGQsIF9hW21hbGlnbmdyb3VwX2pzXzEuTW1sTWFsaWduZ3JvdXAucHJvdG90eXBlLmtpbmRdID0gbWFsaWduZ3JvdXBfanNfMS5NbWxNYWxpZ25ncm91cCwgX2FbbWFsaWdubWFya19qc18xLk1tbE1hbGlnbm1hcmsucHJvdG90eXBlLmtpbmRdID0gbWFsaWdubWFya19qc18xLk1tbE1hbGlnbm1hcmssIF9hW21nbHlwaF9qc18xLk1tbE1nbHlwaC5wcm90b3R5cGUua2luZF0gPSBtZ2x5cGhfanNfMS5NbWxNZ2x5cGgsIF9hW3NlbWFudGljc19qc18xLk1tbFNlbWFudGljcy5wcm90b3R5cGUua2luZF0gPSBzZW1hbnRpY3NfanNfMS5NbWxTZW1hbnRpY3MsIF9hW3NlbWFudGljc19qc18xLk1tbEFubm90YXRpb24ucHJvdG90eXBlLmtpbmRdID0gc2VtYW50aWNzX2pzXzEuTW1sQW5ub3RhdGlvbiwgX2Fbc2VtYW50aWNzX2pzXzEuTW1sQW5ub3RhdGlvblhNTC5wcm90b3R5cGUua2luZF0gPSBzZW1hbnRpY3NfanNfMS5NbWxBbm5vdGF0aW9uWE1MLCBfYVtUZVhBdG9tX2pzXzEuVGVYQXRvbS5wcm90b3R5cGUua2luZF0gPSBUZVhBdG9tX2pzXzEuVGVYQXRvbSwgX2FbbWF0aGNob2ljZV9qc18xLk1hdGhDaG9pY2UucHJvdG90eXBlLmtpbmRdID0gbWF0aGNob2ljZV9qc18xLk1hdGhDaG9pY2UsIF9hW01tbE5vZGVfanNfMS5UZXh0Tm9kZS5wcm90b3R5cGUua2luZF0gPSBNbWxOb2RlX2pzXzEuVGV4dE5vZGUsIF9hW01tbE5vZGVfanNfMS5YTUxOb2RlLnByb3RvdHlwZS5raW5kXSA9IE1tbE5vZGVfanNfMS5YTUxOb2RlLCBfYSk7IiwiXCJ1c2Ugc3RyaWN0XCI7XG5cbnZhciBfX2V4dGVuZHMgPSB0aGlzICYmIHRoaXMuX19leHRlbmRzIHx8IGZ1bmN0aW9uICgpIHtcbiAgdmFyIGV4dGVuZFN0YXRpY3MgPSBmdW5jdGlvbiAoZCwgYikge1xuICAgIGV4dGVuZFN0YXRpY3MgPSBPYmplY3Quc2V0UHJvdG90eXBlT2YgfHwge1xuICAgICAgX19wcm90b19fOiBbXVxuICAgIH0gaW5zdGFuY2VvZiBBcnJheSAmJiBmdW5jdGlvbiAoZCwgYikge1xuICAgICAgZC5fX3Byb3RvX18gPSBiO1xuICAgIH0gfHwgZnVuY3Rpb24gKGQsIGIpIHtcbiAgICAgIGZvciAodmFyIHAgaW4gYikgaWYgKE9iamVjdC5wcm90b3R5cGUuaGFzT3duUHJvcGVydHkuY2FsbChiLCBwKSkgZFtwXSA9IGJbcF07XG4gICAgfTtcbiAgICByZXR1cm4gZXh0ZW5kU3RhdGljcyhkLCBiKTtcbiAgfTtcbiAgcmV0dXJuIGZ1bmN0aW9uIChkLCBiKSB7XG4gICAgaWYgKHR5cGVvZiBiICE9PSBcImZ1bmN0aW9uXCIgJiYgYiAhPT0gbnVsbCkgdGhyb3cgbmV3IFR5cGVFcnJvcihcIkNsYXNzIGV4dGVuZHMgdmFsdWUgXCIgKyBTdHJpbmcoYikgKyBcIiBpcyBub3QgYSBjb25zdHJ1Y3RvciBvciBudWxsXCIpO1xuICAgIGV4dGVuZFN0YXRpY3MoZCwgYik7XG4gICAgZnVuY3Rpb24gX18oKSB7XG4gICAgICB0aGlzLmNvbnN0cnVjdG9yID0gZDtcbiAgICB9XG4gICAgZC5wcm90b3R5cGUgPSBiID09PSBudWxsID8gT2JqZWN0LmNyZWF0ZShiKSA6IChfXy5wcm90b3R5cGUgPSBiLnByb3RvdHlwZSwgbmV3IF9fKCkpO1xuICB9O1xufSgpO1xuT2JqZWN0LmRlZmluZVByb3BlcnR5KGV4cG9ydHMsIFwiX19lc01vZHVsZVwiLCB7XG4gIHZhbHVlOiB0cnVlXG59KTtcbmV4cG9ydHMuTW1sRmFjdG9yeSA9IHZvaWQgMDtcbnZhciBOb2RlRmFjdG9yeV9qc18xID0gcmVxdWlyZShcIi4uL1RyZWUvTm9kZUZhY3RvcnkuanNcIik7XG52YXIgTU1MX2pzXzEgPSByZXF1aXJlKFwiLi9NTUwuanNcIik7XG52YXIgTW1sRmFjdG9yeSA9IGZ1bmN0aW9uIChfc3VwZXIpIHtcbiAgX19leHRlbmRzKE1tbEZhY3RvcnksIF9zdXBlcik7XG4gIGZ1bmN0aW9uIE1tbEZhY3RvcnkoKSB7XG4gICAgcmV0dXJuIF9zdXBlciAhPT0gbnVsbCAmJiBfc3VwZXIuYXBwbHkodGhpcywgYXJndW1lbnRzKSB8fCB0aGlzO1xuICB9XG4gIE9iamVjdC5kZWZpbmVQcm9wZXJ0eShNbWxGYWN0b3J5LnByb3RvdHlwZSwgXCJNTUxcIiwge1xuICAgIGdldDogZnVuY3Rpb24gKCkge1xuICAgICAgcmV0dXJuIHRoaXMubm9kZTtcbiAgICB9LFxuICAgIGVudW1lcmFibGU6IGZhbHNlLFxuICAgIGNvbmZpZ3VyYWJsZTogdHJ1ZVxuICB9KTtcbiAgTW1sRmFjdG9yeS5kZWZhdWx0Tm9kZXMgPSBNTUxfanNfMS5NTUw7XG4gIHJldHVybiBNbWxGYWN0b3J5O1xufShOb2RlRmFjdG9yeV9qc18xLkFic3RyYWN0Tm9kZUZhY3RvcnkpO1xuZXhwb3J0cy5NbWxGYWN0b3J5ID0gTW1sRmFjdG9yeTsiLCJcInVzZSBzdHJpY3RcIjtcblxudmFyIF9fZXh0ZW5kcyA9IHRoaXMgJiYgdGhpcy5fX2V4dGVuZHMgfHwgZnVuY3Rpb24gKCkge1xuICB2YXIgZXh0ZW5kU3RhdGljcyA9IGZ1bmN0aW9uIChkLCBiKSB7XG4gICAgZXh0ZW5kU3RhdGljcyA9IE9iamVjdC5zZXRQcm90b3R5cGVPZiB8fCB7XG4gICAgICBfX3Byb3RvX186IFtdXG4gICAgfSBpbnN0YW5jZW9mIEFycmF5ICYmIGZ1bmN0aW9uIChkLCBiKSB7XG4gICAgICBkLl9fcHJvdG9fXyA9IGI7XG4gICAgfSB8fCBmdW5jdGlvbiAoZCwgYikge1xuICAgICAgZm9yICh2YXIgcCBpbiBiKSBpZiAoT2JqZWN0LnByb3RvdHlwZS5oYXNPd25Qcm9wZXJ0eS5jYWxsKGIsIHApKSBkW3BdID0gYltwXTtcbiAgICB9O1xuICAgIHJldHVybiBleHRlbmRTdGF0aWNzKGQsIGIpO1xuICB9O1xuICByZXR1cm4gZnVuY3Rpb24gKGQsIGIpIHtcbiAgICBpZiAodHlwZW9mIGIgIT09IFwiZnVuY3Rpb25cIiAmJiBiICE9PSBudWxsKSB0aHJvdyBuZXcgVHlwZUVycm9yKFwiQ2xhc3MgZXh0ZW5kcyB2YWx1ZSBcIiArIFN0cmluZyhiKSArIFwiIGlzIG5vdCBhIGNvbnN0cnVjdG9yIG9yIG51bGxcIik7XG4gICAgZXh0ZW5kU3RhdGljcyhkLCBiKTtcbiAgICBmdW5jdGlvbiBfXygpIHtcbiAgICAgIHRoaXMuY29uc3RydWN0b3IgPSBkO1xuICAgIH1cbiAgICBkLnByb3RvdHlwZSA9IGIgPT09IG51bGwgPyBPYmplY3QuY3JlYXRlKGIpIDogKF9fLnByb3RvdHlwZSA9IGIucHJvdG90eXBlLCBuZXcgX18oKSk7XG4gIH07XG59KCk7XG52YXIgX19hc3NpZ24gPSB0aGlzICYmIHRoaXMuX19hc3NpZ24gfHwgZnVuY3Rpb24gKCkge1xuICBfX2Fzc2lnbiA9IE9iamVjdC5hc3NpZ24gfHwgZnVuY3Rpb24gKHQpIHtcbiAgICBmb3IgKHZhciBzLCBpID0gMSwgbiA9IGFyZ3VtZW50cy5sZW5ndGg7IGkgPCBuOyBpKyspIHtcbiAgICAgIHMgPSBhcmd1bWVudHNbaV07XG4gICAgICBmb3IgKHZhciBwIGluIHMpIGlmIChPYmplY3QucHJvdG90eXBlLmhhc093blByb3BlcnR5LmNhbGwocywgcCkpIHRbcF0gPSBzW3BdO1xuICAgIH1cbiAgICByZXR1cm4gdDtcbiAgfTtcbiAgcmV0dXJuIF9fYXNzaWduLmFwcGx5KHRoaXMsIGFyZ3VtZW50cyk7XG59O1xuT2JqZWN0LmRlZmluZVByb3BlcnR5KGV4cG9ydHMsIFwiX19lc01vZHVsZVwiLCB7XG4gIHZhbHVlOiB0cnVlXG59KTtcbmV4cG9ydHMuTW1sTWFsaWduZ3JvdXAgPSB2b2lkIDA7XG52YXIgTW1sTm9kZV9qc18xID0gcmVxdWlyZShcIi4uL01tbE5vZGUuanNcIik7XG52YXIgQXR0cmlidXRlc19qc18xID0gcmVxdWlyZShcIi4uL0F0dHJpYnV0ZXMuanNcIik7XG52YXIgTW1sTWFsaWduZ3JvdXAgPSBmdW5jdGlvbiAoX3N1cGVyKSB7XG4gIF9fZXh0ZW5kcyhNbWxNYWxpZ25ncm91cCwgX3N1cGVyKTtcbiAgZnVuY3Rpb24gTW1sTWFsaWduZ3JvdXAoKSB7XG4gICAgcmV0dXJuIF9zdXBlciAhPT0gbnVsbCAmJiBfc3VwZXIuYXBwbHkodGhpcywgYXJndW1lbnRzKSB8fCB0aGlzO1xuICB9XG4gIE9iamVjdC5kZWZpbmVQcm9wZXJ0eShNbWxNYWxpZ25ncm91cC5wcm90b3R5cGUsIFwia2luZFwiLCB7XG4gICAgZ2V0OiBmdW5jdGlvbiAoKSB7XG4gICAgICByZXR1cm4gJ21hbGlnbmdyb3VwJztcbiAgICB9LFxuICAgIGVudW1lcmFibGU6IGZhbHNlLFxuICAgIGNvbmZpZ3VyYWJsZTogdHJ1ZVxuICB9KTtcbiAgT2JqZWN0LmRlZmluZVByb3BlcnR5KE1tbE1hbGlnbmdyb3VwLnByb3RvdHlwZSwgXCJpc1NwYWNlbGlrZVwiLCB7XG4gICAgZ2V0OiBmdW5jdGlvbiAoKSB7XG4gICAgICByZXR1cm4gdHJ1ZTtcbiAgICB9LFxuICAgIGVudW1lcmFibGU6IGZhbHNlLFxuICAgIGNvbmZpZ3VyYWJsZTogdHJ1ZVxuICB9KTtcbiAgTW1sTWFsaWduZ3JvdXAucHJvdG90eXBlLnNldENoaWxkSW5oZXJpdGVkQXR0cmlidXRlcyA9IGZ1bmN0aW9uIChhdHRyaWJ1dGVzLCBkaXNwbGF5LCBsZXZlbCwgcHJpbWUpIHtcbiAgICBhdHRyaWJ1dGVzID0gdGhpcy5hZGRJbmhlcml0ZWRBdHRyaWJ1dGVzKGF0dHJpYnV0ZXMsIHRoaXMuYXR0cmlidXRlcy5nZXRBbGxBdHRyaWJ1dGVzKCkpO1xuICAgIF9zdXBlci5wcm90b3R5cGUuc2V0Q2hpbGRJbmhlcml0ZWRBdHRyaWJ1dGVzLmNhbGwodGhpcywgYXR0cmlidXRlcywgZGlzcGxheSwgbGV2ZWwsIHByaW1lKTtcbiAgfTtcbiAgTW1sTWFsaWduZ3JvdXAuZGVmYXVsdHMgPSBfX2Fzc2lnbihfX2Fzc2lnbih7fSwgTW1sTm9kZV9qc18xLkFic3RyYWN0TW1sTGF5b3V0Tm9kZS5kZWZhdWx0cyksIHtcbiAgICBncm91cGFsaWduOiBBdHRyaWJ1dGVzX2pzXzEuSU5IRVJJVFxuICB9KTtcbiAgcmV0dXJuIE1tbE1hbGlnbmdyb3VwO1xufShNbWxOb2RlX2pzXzEuQWJzdHJhY3RNbWxMYXlvdXROb2RlKTtcbmV4cG9ydHMuTW1sTWFsaWduZ3JvdXAgPSBNbWxNYWxpZ25ncm91cDsiLCJcInVzZSBzdHJpY3RcIjtcblxudmFyIF9fZXh0ZW5kcyA9IHRoaXMgJiYgdGhpcy5fX2V4dGVuZHMgfHwgZnVuY3Rpb24gKCkge1xuICB2YXIgZXh0ZW5kU3RhdGljcyA9IGZ1bmN0aW9uIChkLCBiKSB7XG4gICAgZXh0ZW5kU3RhdGljcyA9IE9iamVjdC5zZXRQcm90b3R5cGVPZiB8fCB7XG4gICAgICBfX3Byb3RvX186IFtdXG4gICAgfSBpbnN0YW5jZW9mIEFycmF5ICYmIGZ1bmN0aW9uIChkLCBiKSB7XG4gICAgICBkLl9fcHJvdG9fXyA9IGI7XG4gICAgfSB8fCBmdW5jdGlvbiAoZCwgYikge1xuICAgICAgZm9yICh2YXIgcCBpbiBiKSBpZiAoT2JqZWN0LnByb3RvdHlwZS5oYXNPd25Qcm9wZXJ0eS5jYWxsKGIsIHApKSBkW3BdID0gYltwXTtcbiAgICB9O1xuICAgIHJldHVybiBleHRlbmRTdGF0aWNzKGQsIGIpO1xuICB9O1xuICByZXR1cm4gZnVuY3Rpb24gKGQsIGIpIHtcbiAgICBpZiAodHlwZW9mIGIgIT09IFwiZnVuY3Rpb25cIiAmJiBiICE9PSBudWxsKSB0aHJvdyBuZXcgVHlwZUVycm9yKFwiQ2xhc3MgZXh0ZW5kcyB2YWx1ZSBcIiArIFN0cmluZyhiKSArIFwiIGlzIG5vdCBhIGNvbnN0cnVjdG9yIG9yIG51bGxcIik7XG4gICAgZXh0ZW5kU3RhdGljcyhkLCBiKTtcbiAgICBmdW5jdGlvbiBfXygpIHtcbiAgICAgIHRoaXMuY29uc3RydWN0b3IgPSBkO1xuICAgIH1cbiAgICBkLnByb3RvdHlwZSA9IGIgPT09IG51bGwgPyBPYmplY3QuY3JlYXRlKGIpIDogKF9fLnByb3RvdHlwZSA9IGIucHJvdG90eXBlLCBuZXcgX18oKSk7XG4gIH07XG59KCk7XG52YXIgX19hc3NpZ24gPSB0aGlzICYmIHRoaXMuX19hc3NpZ24gfHwgZnVuY3Rpb24gKCkge1xuICBfX2Fzc2lnbiA9IE9iamVjdC5hc3NpZ24gfHwgZnVuY3Rpb24gKHQpIHtcbiAgICBmb3IgKHZhciBzLCBpID0gMSwgbiA9IGFyZ3VtZW50cy5sZW5ndGg7IGkgPCBuOyBpKyspIHtcbiAgICAgIHMgPSBhcmd1bWVudHNbaV07XG4gICAgICBmb3IgKHZhciBwIGluIHMpIGlmIChPYmplY3QucHJvdG90eXBlLmhhc093blByb3BlcnR5LmNhbGwocywgcCkpIHRbcF0gPSBzW3BdO1xuICAgIH1cbiAgICByZXR1cm4gdDtcbiAgfTtcbiAgcmV0dXJuIF9fYXNzaWduLmFwcGx5KHRoaXMsIGFyZ3VtZW50cyk7XG59O1xuT2JqZWN0LmRlZmluZVByb3BlcnR5KGV4cG9ydHMsIFwiX19lc01vZHVsZVwiLCB7XG4gIHZhbHVlOiB0cnVlXG59KTtcbmV4cG9ydHMuTW1sTWFsaWdubWFyayA9IHZvaWQgMDtcbnZhciBNbWxOb2RlX2pzXzEgPSByZXF1aXJlKFwiLi4vTW1sTm9kZS5qc1wiKTtcbnZhciBNbWxNYWxpZ25tYXJrID0gZnVuY3Rpb24gKF9zdXBlcikge1xuICBfX2V4dGVuZHMoTW1sTWFsaWdubWFyaywgX3N1cGVyKTtcbiAgZnVuY3Rpb24gTW1sTWFsaWdubWFyaygpIHtcbiAgICByZXR1cm4gX3N1cGVyICE9PSBudWxsICYmIF9zdXBlci5hcHBseSh0aGlzLCBhcmd1bWVudHMpIHx8IHRoaXM7XG4gIH1cbiAgT2JqZWN0LmRlZmluZVByb3BlcnR5KE1tbE1hbGlnbm1hcmsucHJvdG90eXBlLCBcImtpbmRcIiwge1xuICAgIGdldDogZnVuY3Rpb24gKCkge1xuICAgICAgcmV0dXJuICdtYWxpZ25tYXJrJztcbiAgICB9LFxuICAgIGVudW1lcmFibGU6IGZhbHNlLFxuICAgIGNvbmZpZ3VyYWJsZTogdHJ1ZVxuICB9KTtcbiAgT2JqZWN0LmRlZmluZVByb3BlcnR5KE1tbE1hbGlnbm1hcmsucHJvdG90eXBlLCBcImFyaXR5XCIsIHtcbiAgICBnZXQ6IGZ1bmN0aW9uICgpIHtcbiAgICAgIHJldHVybiAwO1xuICAgIH0sXG4gICAgZW51bWVyYWJsZTogZmFsc2UsXG4gICAgY29uZmlndXJhYmxlOiB0cnVlXG4gIH0pO1xuICBPYmplY3QuZGVmaW5lUHJvcGVydHkoTW1sTWFsaWdubWFyay5wcm90b3R5cGUsIFwiaXNTcGFjZWxpa2VcIiwge1xuICAgIGdldDogZnVuY3Rpb24gKCkge1xuICAgICAgcmV0dXJuIHRydWU7XG4gICAgfSxcbiAgICBlbnVtZXJhYmxlOiBmYWxzZSxcbiAgICBjb25maWd1cmFibGU6IHRydWVcbiAgfSk7XG4gIE1tbE1hbGlnbm1hcmsuZGVmYXVsdHMgPSBfX2Fzc2lnbihfX2Fzc2lnbih7fSwgTW1sTm9kZV9qc18xLkFic3RyYWN0TW1sTm9kZS5kZWZhdWx0cyksIHtcbiAgICBlZGdlOiAnbGVmdCdcbiAgfSk7XG4gIHJldHVybiBNbWxNYWxpZ25tYXJrO1xufShNbWxOb2RlX2pzXzEuQWJzdHJhY3RNbWxOb2RlKTtcbmV4cG9ydHMuTW1sTWFsaWdubWFyayA9IE1tbE1hbGlnbm1hcms7IiwiXCJ1c2Ugc3RyaWN0XCI7XG5cbnZhciBfX2V4dGVuZHMgPSB0aGlzICYmIHRoaXMuX19leHRlbmRzIHx8IGZ1bmN0aW9uICgpIHtcbiAgdmFyIGV4dGVuZFN0YXRpY3MgPSBmdW5jdGlvbiAoZCwgYikge1xuICAgIGV4dGVuZFN0YXRpY3MgPSBPYmplY3Quc2V0UHJvdG90eXBlT2YgfHwge1xuICAgICAgX19wcm90b19fOiBbXVxuICAgIH0gaW5zdGFuY2VvZiBBcnJheSAmJiBmdW5jdGlvbiAoZCwgYikge1xuICAgICAgZC5fX3Byb3RvX18gPSBiO1xuICAgIH0gfHwgZnVuY3Rpb24gKGQsIGIpIHtcbiAgICAgIGZvciAodmFyIHAgaW4gYikgaWYgKE9iamVjdC5wcm90b3R5cGUuaGFzT3duUHJvcGVydHkuY2FsbChiLCBwKSkgZFtwXSA9IGJbcF07XG4gICAgfTtcbiAgICByZXR1cm4gZXh0ZW5kU3RhdGljcyhkLCBiKTtcbiAgfTtcbiAgcmV0dXJuIGZ1bmN0aW9uIChkLCBiKSB7XG4gICAgaWYgKHR5cGVvZiBiICE9PSBcImZ1bmN0aW9uXCIgJiYgYiAhPT0gbnVsbCkgdGhyb3cgbmV3IFR5cGVFcnJvcihcIkNsYXNzIGV4dGVuZHMgdmFsdWUgXCIgKyBTdHJpbmcoYikgKyBcIiBpcyBub3QgYSBjb25zdHJ1Y3RvciBvciBudWxsXCIpO1xuICAgIGV4dGVuZFN0YXRpY3MoZCwgYik7XG4gICAgZnVuY3Rpb24gX18oKSB7XG4gICAgICB0aGlzLmNvbnN0cnVjdG9yID0gZDtcbiAgICB9XG4gICAgZC5wcm90b3R5cGUgPSBiID09PSBudWxsID8gT2JqZWN0LmNyZWF0ZShiKSA6IChfXy5wcm90b3R5cGUgPSBiLnByb3RvdHlwZSwgbmV3IF9fKCkpO1xuICB9O1xufSgpO1xudmFyIF9fYXNzaWduID0gdGhpcyAmJiB0aGlzLl9fYXNzaWduIHx8IGZ1bmN0aW9uICgpIHtcbiAgX19hc3NpZ24gPSBPYmplY3QuYXNzaWduIHx8IGZ1bmN0aW9uICh0KSB7XG4gICAgZm9yICh2YXIgcywgaSA9IDEsIG4gPSBhcmd1bWVudHMubGVuZ3RoOyBpIDwgbjsgaSsrKSB7XG4gICAgICBzID0gYXJndW1lbnRzW2ldO1xuICAgICAgZm9yICh2YXIgcCBpbiBzKSBpZiAoT2JqZWN0LnByb3RvdHlwZS5oYXNPd25Qcm9wZXJ0eS5jYWxsKHMsIHApKSB0W3BdID0gc1twXTtcbiAgICB9XG4gICAgcmV0dXJuIHQ7XG4gIH07XG4gIHJldHVybiBfX2Fzc2lnbi5hcHBseSh0aGlzLCBhcmd1bWVudHMpO1xufTtcbk9iamVjdC5kZWZpbmVQcm9wZXJ0eShleHBvcnRzLCBcIl9fZXNNb2R1bGVcIiwge1xuICB2YWx1ZTogdHJ1ZVxufSk7XG5leHBvcnRzLk1hdGhDaG9pY2UgPSB2b2lkIDA7XG52YXIgTW1sTm9kZV9qc18xID0gcmVxdWlyZShcIi4uL01tbE5vZGUuanNcIik7XG52YXIgTWF0aENob2ljZSA9IGZ1bmN0aW9uIChfc3VwZXIpIHtcbiAgX19leHRlbmRzKE1hdGhDaG9pY2UsIF9zdXBlcik7XG4gIGZ1bmN0aW9uIE1hdGhDaG9pY2UoKSB7XG4gICAgcmV0dXJuIF9zdXBlciAhPT0gbnVsbCAmJiBfc3VwZXIuYXBwbHkodGhpcywgYXJndW1lbnRzKSB8fCB0aGlzO1xuICB9XG4gIE9iamVjdC5kZWZpbmVQcm9wZXJ0eShNYXRoQ2hvaWNlLnByb3RvdHlwZSwgXCJraW5kXCIsIHtcbiAgICBnZXQ6IGZ1bmN0aW9uICgpIHtcbiAgICAgIHJldHVybiAnTWF0aENob2ljZSc7XG4gICAgfSxcbiAgICBlbnVtZXJhYmxlOiBmYWxzZSxcbiAgICBjb25maWd1cmFibGU6IHRydWVcbiAgfSk7XG4gIE9iamVjdC5kZWZpbmVQcm9wZXJ0eShNYXRoQ2hvaWNlLnByb3RvdHlwZSwgXCJhcml0eVwiLCB7XG4gICAgZ2V0OiBmdW5jdGlvbiAoKSB7XG4gICAgICByZXR1cm4gNDtcbiAgICB9LFxuICAgIGVudW1lcmFibGU6IGZhbHNlLFxuICAgIGNvbmZpZ3VyYWJsZTogdHJ1ZVxuICB9KTtcbiAgT2JqZWN0LmRlZmluZVByb3BlcnR5KE1hdGhDaG9pY2UucHJvdG90eXBlLCBcIm5vdFBhcmVudFwiLCB7XG4gICAgZ2V0OiBmdW5jdGlvbiAoKSB7XG4gICAgICByZXR1cm4gdHJ1ZTtcbiAgICB9LFxuICAgIGVudW1lcmFibGU6IGZhbHNlLFxuICAgIGNvbmZpZ3VyYWJsZTogdHJ1ZVxuICB9KTtcbiAgTWF0aENob2ljZS5wcm90b3R5cGUuc2V0SW5oZXJpdGVkQXR0cmlidXRlcyA9IGZ1bmN0aW9uIChhdHRyaWJ1dGVzLCBkaXNwbGF5LCBsZXZlbCwgcHJpbWUpIHtcbiAgICB2YXIgc2VsZWN0aW9uID0gZGlzcGxheSA/IDAgOiBNYXRoLm1heCgwLCBNYXRoLm1pbihsZXZlbCwgMikpICsgMTtcbiAgICB2YXIgY2hpbGQgPSB0aGlzLmNoaWxkTm9kZXNbc2VsZWN0aW9uXSB8fCB0aGlzLmZhY3RvcnkuY3JlYXRlKCdtcm93Jyk7XG4gICAgdGhpcy5wYXJlbnQucmVwbGFjZUNoaWxkKGNoaWxkLCB0aGlzKTtcbiAgICBjaGlsZC5zZXRJbmhlcml0ZWRBdHRyaWJ1dGVzKGF0dHJpYnV0ZXMsIGRpc3BsYXksIGxldmVsLCBwcmltZSk7XG4gIH07XG4gIE1hdGhDaG9pY2UuZGVmYXVsdHMgPSBfX2Fzc2lnbih7fSwgTW1sTm9kZV9qc18xLkFic3RyYWN0TW1sQmFzZU5vZGUuZGVmYXVsdHMpO1xuICByZXR1cm4gTWF0aENob2ljZTtcbn0oTW1sTm9kZV9qc18xLkFic3RyYWN0TW1sQmFzZU5vZGUpO1xuZXhwb3J0cy5NYXRoQ2hvaWNlID0gTWF0aENob2ljZTsiLCJcInVzZSBzdHJpY3RcIjtcblxudmFyIF9fZXh0ZW5kcyA9IHRoaXMgJiYgdGhpcy5fX2V4dGVuZHMgfHwgZnVuY3Rpb24gKCkge1xuICB2YXIgZXh0ZW5kU3RhdGljcyA9IGZ1bmN0aW9uIChkLCBiKSB7XG4gICAgZXh0ZW5kU3RhdGljcyA9IE9iamVjdC5zZXRQcm90b3R5cGVPZiB8fCB7XG4gICAgICBfX3Byb3RvX186IFtdXG4gICAgfSBpbnN0YW5jZW9mIEFycmF5ICYmIGZ1bmN0aW9uIChkLCBiKSB7XG4gICAgICBkLl9fcHJvdG9fXyA9IGI7XG4gICAgfSB8fCBmdW5jdGlvbiAoZCwgYikge1xuICAgICAgZm9yICh2YXIgcCBpbiBiKSBpZiAoT2JqZWN0LnByb3RvdHlwZS5oYXNPd25Qcm9wZXJ0eS5jYWxsKGIsIHApKSBkW3BdID0gYltwXTtcbiAgICB9O1xuICAgIHJldHVybiBleHRlbmRTdGF0aWNzKGQsIGIpO1xuICB9O1xuICByZXR1cm4gZnVuY3Rpb24gKGQsIGIpIHtcbiAgICBpZiAodHlwZW9mIGIgIT09IFwiZnVuY3Rpb25cIiAmJiBiICE9PSBudWxsKSB0aHJvdyBuZXcgVHlwZUVycm9yKFwiQ2xhc3MgZXh0ZW5kcyB2YWx1ZSBcIiArIFN0cmluZyhiKSArIFwiIGlzIG5vdCBhIGNvbnN0cnVjdG9yIG9yIG51bGxcIik7XG4gICAgZXh0ZW5kU3RhdGljcyhkLCBiKTtcbiAgICBmdW5jdGlvbiBfXygpIHtcbiAgICAgIHRoaXMuY29uc3RydWN0b3IgPSBkO1xuICAgIH1cbiAgICBkLnByb3RvdHlwZSA9IGIgPT09IG51bGwgPyBPYmplY3QuY3JlYXRlKGIpIDogKF9fLnByb3RvdHlwZSA9IGIucHJvdG90eXBlLCBuZXcgX18oKSk7XG4gIH07XG59KCk7XG52YXIgX19hc3NpZ24gPSB0aGlzICYmIHRoaXMuX19hc3NpZ24gfHwgZnVuY3Rpb24gKCkge1xuICBfX2Fzc2lnbiA9IE9iamVjdC5hc3NpZ24gfHwgZnVuY3Rpb24gKHQpIHtcbiAgICBmb3IgKHZhciBzLCBpID0gMSwgbiA9IGFyZ3VtZW50cy5sZW5ndGg7IGkgPCBuOyBpKyspIHtcbiAgICAgIHMgPSBhcmd1bWVudHNbaV07XG4gICAgICBmb3IgKHZhciBwIGluIHMpIGlmIChPYmplY3QucHJvdG90eXBlLmhhc093blByb3BlcnR5LmNhbGwocywgcCkpIHRbcF0gPSBzW3BdO1xuICAgIH1cbiAgICByZXR1cm4gdDtcbiAgfTtcbiAgcmV0dXJuIF9fYXNzaWduLmFwcGx5KHRoaXMsIGFyZ3VtZW50cyk7XG59O1xuT2JqZWN0LmRlZmluZVByb3BlcnR5KGV4cG9ydHMsIFwiX19lc01vZHVsZVwiLCB7XG4gIHZhbHVlOiB0cnVlXG59KTtcbmV4cG9ydHMuTW1sTWVycm9yID0gdm9pZCAwO1xudmFyIE1tbE5vZGVfanNfMSA9IHJlcXVpcmUoXCIuLi9NbWxOb2RlLmpzXCIpO1xudmFyIE1tbE1lcnJvciA9IGZ1bmN0aW9uIChfc3VwZXIpIHtcbiAgX19leHRlbmRzKE1tbE1lcnJvciwgX3N1cGVyKTtcbiAgZnVuY3Rpb24gTW1sTWVycm9yKCkge1xuICAgIHZhciBfdGhpcyA9IF9zdXBlciAhPT0gbnVsbCAmJiBfc3VwZXIuYXBwbHkodGhpcywgYXJndW1lbnRzKSB8fCB0aGlzO1xuICAgIF90aGlzLnRleGNsYXNzID0gTW1sTm9kZV9qc18xLlRFWENMQVNTLk9SRDtcbiAgICByZXR1cm4gX3RoaXM7XG4gIH1cbiAgT2JqZWN0LmRlZmluZVByb3BlcnR5KE1tbE1lcnJvci5wcm90b3R5cGUsIFwia2luZFwiLCB7XG4gICAgZ2V0OiBmdW5jdGlvbiAoKSB7XG4gICAgICByZXR1cm4gJ21lcnJvcic7XG4gICAgfSxcbiAgICBlbnVtZXJhYmxlOiBmYWxzZSxcbiAgICBjb25maWd1cmFibGU6IHRydWVcbiAgfSk7XG4gIE9iamVjdC5kZWZpbmVQcm9wZXJ0eShNbWxNZXJyb3IucHJvdG90eXBlLCBcImFyaXR5XCIsIHtcbiAgICBnZXQ6IGZ1bmN0aW9uICgpIHtcbiAgICAgIHJldHVybiAtMTtcbiAgICB9LFxuICAgIGVudW1lcmFibGU6IGZhbHNlLFxuICAgIGNvbmZpZ3VyYWJsZTogdHJ1ZVxuICB9KTtcbiAgT2JqZWN0LmRlZmluZVByb3BlcnR5KE1tbE1lcnJvci5wcm90b3R5cGUsIFwibGluZWJyZWFrQ29udGFpbmVyXCIsIHtcbiAgICBnZXQ6IGZ1bmN0aW9uICgpIHtcbiAgICAgIHJldHVybiB0cnVlO1xuICAgIH0sXG4gICAgZW51bWVyYWJsZTogZmFsc2UsXG4gICAgY29uZmlndXJhYmxlOiB0cnVlXG4gIH0pO1xuICBNbWxNZXJyb3IuZGVmYXVsdHMgPSBfX2Fzc2lnbih7fSwgTW1sTm9kZV9qc18xLkFic3RyYWN0TW1sTm9kZS5kZWZhdWx0cyk7XG4gIHJldHVybiBNbWxNZXJyb3I7XG59KE1tbE5vZGVfanNfMS5BYnN0cmFjdE1tbE5vZGUpO1xuZXhwb3J0cy5NbWxNZXJyb3IgPSBNbWxNZXJyb3I7IiwiXCJ1c2Ugc3RyaWN0XCI7XG5cbnZhciBfX2V4dGVuZHMgPSB0aGlzICYmIHRoaXMuX19leHRlbmRzIHx8IGZ1bmN0aW9uICgpIHtcbiAgdmFyIGV4dGVuZFN0YXRpY3MgPSBmdW5jdGlvbiAoZCwgYikge1xuICAgIGV4dGVuZFN0YXRpY3MgPSBPYmplY3Quc2V0UHJvdG90eXBlT2YgfHwge1xuICAgICAgX19wcm90b19fOiBbXVxuICAgIH0gaW5zdGFuY2VvZiBBcnJheSAmJiBmdW5jdGlvbiAoZCwgYikge1xuICAgICAgZC5fX3Byb3RvX18gPSBiO1xuICAgIH0gfHwgZnVuY3Rpb24gKGQsIGIpIHtcbiAgICAgIGZvciAodmFyIHAgaW4gYikgaWYgKE9iamVjdC5wcm90b3R5cGUuaGFzT3duUHJvcGVydHkuY2FsbChiLCBwKSkgZFtwXSA9IGJbcF07XG4gICAgfTtcbiAgICByZXR1cm4gZXh0ZW5kU3RhdGljcyhkLCBiKTtcbiAgfTtcbiAgcmV0dXJuIGZ1bmN0aW9uIChkLCBiKSB7XG4gICAgaWYgKHR5cGVvZiBiICE9PSBcImZ1bmN0aW9uXCIgJiYgYiAhPT0gbnVsbCkgdGhyb3cgbmV3IFR5cGVFcnJvcihcIkNsYXNzIGV4dGVuZHMgdmFsdWUgXCIgKyBTdHJpbmcoYikgKyBcIiBpcyBub3QgYSBjb25zdHJ1Y3RvciBvciBudWxsXCIpO1xuICAgIGV4dGVuZFN0YXRpY3MoZCwgYik7XG4gICAgZnVuY3Rpb24gX18oKSB7XG4gICAgICB0aGlzLmNvbnN0cnVjdG9yID0gZDtcbiAgICB9XG4gICAgZC5wcm90b3R5cGUgPSBiID09PSBudWxsID8gT2JqZWN0LmNyZWF0ZShiKSA6IChfXy5wcm90b3R5cGUgPSBiLnByb3RvdHlwZSwgbmV3IF9fKCkpO1xuICB9O1xufSgpO1xudmFyIF9fYXNzaWduID0gdGhpcyAmJiB0aGlzLl9fYXNzaWduIHx8IGZ1bmN0aW9uICgpIHtcbiAgX19hc3NpZ24gPSBPYmplY3QuYXNzaWduIHx8IGZ1bmN0aW9uICh0KSB7XG4gICAgZm9yICh2YXIgcywgaSA9IDEsIG4gPSBhcmd1bWVudHMubGVuZ3RoOyBpIDwgbjsgaSsrKSB7XG4gICAgICBzID0gYXJndW1lbnRzW2ldO1xuICAgICAgZm9yICh2YXIgcCBpbiBzKSBpZiAoT2JqZWN0LnByb3RvdHlwZS5oYXNPd25Qcm9wZXJ0eS5jYWxsKHMsIHApKSB0W3BdID0gc1twXTtcbiAgICB9XG4gICAgcmV0dXJuIHQ7XG4gIH07XG4gIHJldHVybiBfX2Fzc2lnbi5hcHBseSh0aGlzLCBhcmd1bWVudHMpO1xufTtcbk9iamVjdC5kZWZpbmVQcm9wZXJ0eShleHBvcnRzLCBcIl9fZXNNb2R1bGVcIiwge1xuICB2YWx1ZTogdHJ1ZVxufSk7XG5leHBvcnRzLk1tbE1waGFudG9tID0gdm9pZCAwO1xudmFyIE1tbE5vZGVfanNfMSA9IHJlcXVpcmUoXCIuLi9NbWxOb2RlLmpzXCIpO1xudmFyIE1tbE1waGFudG9tID0gZnVuY3Rpb24gKF9zdXBlcikge1xuICBfX2V4dGVuZHMoTW1sTXBoYW50b20sIF9zdXBlcik7XG4gIGZ1bmN0aW9uIE1tbE1waGFudG9tKCkge1xuICAgIHZhciBfdGhpcyA9IF9zdXBlciAhPT0gbnVsbCAmJiBfc3VwZXIuYXBwbHkodGhpcywgYXJndW1lbnRzKSB8fCB0aGlzO1xuICAgIF90aGlzLnRleGNsYXNzID0gTW1sTm9kZV9qc18xLlRFWENMQVNTLk9SRDtcbiAgICByZXR1cm4gX3RoaXM7XG4gIH1cbiAgT2JqZWN0LmRlZmluZVByb3BlcnR5KE1tbE1waGFudG9tLnByb3RvdHlwZSwgXCJraW5kXCIsIHtcbiAgICBnZXQ6IGZ1bmN0aW9uICgpIHtcbiAgICAgIHJldHVybiAnbXBoYW50b20nO1xuICAgIH0sXG4gICAgZW51bWVyYWJsZTogZmFsc2UsXG4gICAgY29uZmlndXJhYmxlOiB0cnVlXG4gIH0pO1xuICBNbWxNcGhhbnRvbS5kZWZhdWx0cyA9IF9fYXNzaWduKHt9LCBNbWxOb2RlX2pzXzEuQWJzdHJhY3RNbWxMYXlvdXROb2RlLmRlZmF1bHRzKTtcbiAgcmV0dXJuIE1tbE1waGFudG9tO1xufShNbWxOb2RlX2pzXzEuQWJzdHJhY3RNbWxMYXlvdXROb2RlKTtcbmV4cG9ydHMuTW1sTXBoYW50b20gPSBNbWxNcGhhbnRvbTsiLCJcInVzZSBzdHJpY3RcIjtcblxudmFyIF9fZXh0ZW5kcyA9IHRoaXMgJiYgdGhpcy5fX2V4dGVuZHMgfHwgZnVuY3Rpb24gKCkge1xuICB2YXIgZXh0ZW5kU3RhdGljcyA9IGZ1bmN0aW9uIChkLCBiKSB7XG4gICAgZXh0ZW5kU3RhdGljcyA9IE9iamVjdC5zZXRQcm90b3R5cGVPZiB8fCB7XG4gICAgICBfX3Byb3RvX186IFtdXG4gICAgfSBpbnN0YW5jZW9mIEFycmF5ICYmIGZ1bmN0aW9uIChkLCBiKSB7XG4gICAgICBkLl9fcHJvdG9fXyA9IGI7XG4gICAgfSB8fCBmdW5jdGlvbiAoZCwgYikge1xuICAgICAgZm9yICh2YXIgcCBpbiBiKSBpZiAoT2JqZWN0LnByb3RvdHlwZS5oYXNPd25Qcm9wZXJ0eS5jYWxsKGIsIHApKSBkW3BdID0gYltwXTtcbiAgICB9O1xuICAgIHJldHVybiBleHRlbmRTdGF0aWNzKGQsIGIpO1xuICB9O1xuICByZXR1cm4gZnVuY3Rpb24gKGQsIGIpIHtcbiAgICBpZiAodHlwZW9mIGIgIT09IFwiZnVuY3Rpb25cIiAmJiBiICE9PSBudWxsKSB0aHJvdyBuZXcgVHlwZUVycm9yKFwiQ2xhc3MgZXh0ZW5kcyB2YWx1ZSBcIiArIFN0cmluZyhiKSArIFwiIGlzIG5vdCBhIGNvbnN0cnVjdG9yIG9yIG51bGxcIik7XG4gICAgZXh0ZW5kU3RhdGljcyhkLCBiKTtcbiAgICBmdW5jdGlvbiBfXygpIHtcbiAgICAgIHRoaXMuY29uc3RydWN0b3IgPSBkO1xuICAgIH1cbiAgICBkLnByb3RvdHlwZSA9IGIgPT09IG51bGwgPyBPYmplY3QuY3JlYXRlKGIpIDogKF9fLnByb3RvdHlwZSA9IGIucHJvdG90eXBlLCBuZXcgX18oKSk7XG4gIH07XG59KCk7XG52YXIgX19hc3NpZ24gPSB0aGlzICYmIHRoaXMuX19hc3NpZ24gfHwgZnVuY3Rpb24gKCkge1xuICBfX2Fzc2lnbiA9IE9iamVjdC5hc3NpZ24gfHwgZnVuY3Rpb24gKHQpIHtcbiAgICBmb3IgKHZhciBzLCBpID0gMSwgbiA9IGFyZ3VtZW50cy5sZW5ndGg7IGkgPCBuOyBpKyspIHtcbiAgICAgIHMgPSBhcmd1bWVudHNbaV07XG4gICAgICBmb3IgKHZhciBwIGluIHMpIGlmIChPYmplY3QucHJvdG90eXBlLmhhc093blByb3BlcnR5LmNhbGwocywgcCkpIHRbcF0gPSBzW3BdO1xuICAgIH1cbiAgICByZXR1cm4gdDtcbiAgfTtcbiAgcmV0dXJuIF9fYXNzaWduLmFwcGx5KHRoaXMsIGFyZ3VtZW50cyk7XG59O1xuT2JqZWN0LmRlZmluZVByb3BlcnR5KGV4cG9ydHMsIFwiX19lc01vZHVsZVwiLCB7XG4gIHZhbHVlOiB0cnVlXG59KTtcbmV4cG9ydHMuTW1sTXN0eWxlID0gdm9pZCAwO1xudmFyIE1tbE5vZGVfanNfMSA9IHJlcXVpcmUoXCIuLi9NbWxOb2RlLmpzXCIpO1xudmFyIEF0dHJpYnV0ZXNfanNfMSA9IHJlcXVpcmUoXCIuLi9BdHRyaWJ1dGVzLmpzXCIpO1xudmFyIE1tbE1zdHlsZSA9IGZ1bmN0aW9uIChfc3VwZXIpIHtcbiAgX19leHRlbmRzKE1tbE1zdHlsZSwgX3N1cGVyKTtcbiAgZnVuY3Rpb24gTW1sTXN0eWxlKCkge1xuICAgIHJldHVybiBfc3VwZXIgIT09IG51bGwgJiYgX3N1cGVyLmFwcGx5KHRoaXMsIGFyZ3VtZW50cykgfHwgdGhpcztcbiAgfVxuICBPYmplY3QuZGVmaW5lUHJvcGVydHkoTW1sTXN0eWxlLnByb3RvdHlwZSwgXCJraW5kXCIsIHtcbiAgICBnZXQ6IGZ1bmN0aW9uICgpIHtcbiAgICAgIHJldHVybiAnbXN0eWxlJztcbiAgICB9LFxuICAgIGVudW1lcmFibGU6IGZhbHNlLFxuICAgIGNvbmZpZ3VyYWJsZTogdHJ1ZVxuICB9KTtcbiAgT2JqZWN0LmRlZmluZVByb3BlcnR5KE1tbE1zdHlsZS5wcm90b3R5cGUsIFwibm90UGFyZW50XCIsIHtcbiAgICBnZXQ6IGZ1bmN0aW9uICgpIHtcbiAgICAgIHJldHVybiB0aGlzLmNoaWxkTm9kZXNbMF0gJiYgdGhpcy5jaGlsZE5vZGVzWzBdLmNoaWxkTm9kZXMubGVuZ3RoID09PSAxO1xuICAgIH0sXG4gICAgZW51bWVyYWJsZTogZmFsc2UsXG4gICAgY29uZmlndXJhYmxlOiB0cnVlXG4gIH0pO1xuICBNbWxNc3R5bGUucHJvdG90eXBlLnNldENoaWxkSW5oZXJpdGVkQXR0cmlidXRlcyA9IGZ1bmN0aW9uIChhdHRyaWJ1dGVzLCBkaXNwbGF5LCBsZXZlbCwgcHJpbWUpIHtcbiAgICB2YXIgc2NyaXB0bGV2ZWwgPSB0aGlzLmF0dHJpYnV0ZXMuZ2V0RXhwbGljaXQoJ3NjcmlwdGxldmVsJyk7XG4gICAgaWYgKHNjcmlwdGxldmVsICE9IG51bGwpIHtcbiAgICAgIHNjcmlwdGxldmVsID0gc2NyaXB0bGV2ZWwudG9TdHJpbmcoKTtcbiAgICAgIGlmIChzY3JpcHRsZXZlbC5tYXRjaCgvXlxccypbLStdLykpIHtcbiAgICAgICAgbGV2ZWwgKz0gcGFyc2VJbnQoc2NyaXB0bGV2ZWwpO1xuICAgICAgfSBlbHNlIHtcbiAgICAgICAgbGV2ZWwgPSBwYXJzZUludChzY3JpcHRsZXZlbCk7XG4gICAgICB9XG4gICAgICBwcmltZSA9IGZhbHNlO1xuICAgIH1cbiAgICB2YXIgZGlzcGxheXN0eWxlID0gdGhpcy5hdHRyaWJ1dGVzLmdldEV4cGxpY2l0KCdkaXNwbGF5c3R5bGUnKTtcbiAgICBpZiAoZGlzcGxheXN0eWxlICE9IG51bGwpIHtcbiAgICAgIGRpc3BsYXkgPSBkaXNwbGF5c3R5bGUgPT09IHRydWU7XG4gICAgICBwcmltZSA9IGZhbHNlO1xuICAgIH1cbiAgICB2YXIgY3JhbXBlZCA9IHRoaXMuYXR0cmlidXRlcy5nZXRFeHBsaWNpdCgnZGF0YS1jcmFtcGVkJyk7XG4gICAgaWYgKGNyYW1wZWQgIT0gbnVsbCkge1xuICAgICAgcHJpbWUgPSBjcmFtcGVkO1xuICAgIH1cbiAgICBhdHRyaWJ1dGVzID0gdGhpcy5hZGRJbmhlcml0ZWRBdHRyaWJ1dGVzKGF0dHJpYnV0ZXMsIHRoaXMuYXR0cmlidXRlcy5nZXRBbGxBdHRyaWJ1dGVzKCkpO1xuICAgIHRoaXMuY2hpbGROb2Rlc1swXS5zZXRJbmhlcml0ZWRBdHRyaWJ1dGVzKGF0dHJpYnV0ZXMsIGRpc3BsYXksIGxldmVsLCBwcmltZSk7XG4gIH07XG4gIE1tbE1zdHlsZS5kZWZhdWx0cyA9IF9fYXNzaWduKF9fYXNzaWduKHt9LCBNbWxOb2RlX2pzXzEuQWJzdHJhY3RNbWxMYXlvdXROb2RlLmRlZmF1bHRzKSwge1xuICAgIHNjcmlwdGxldmVsOiBBdHRyaWJ1dGVzX2pzXzEuSU5IRVJJVCxcbiAgICBkaXNwbGF5c3R5bGU6IEF0dHJpYnV0ZXNfanNfMS5JTkhFUklULFxuICAgIHNjcmlwdHNpemVtdWx0aXBsaWVyOiAxIC8gTWF0aC5zcXJ0KDIpLFxuICAgIHNjcmlwdG1pbnNpemU6ICc4cHgnLFxuICAgIG1hdGhiYWNrZ3JvdW5kOiBBdHRyaWJ1dGVzX2pzXzEuSU5IRVJJVCxcbiAgICBtYXRoY29sb3I6IEF0dHJpYnV0ZXNfanNfMS5JTkhFUklULFxuICAgIGRpcjogQXR0cmlidXRlc19qc18xLklOSEVSSVQsXG4gICAgaW5maXhsaW5lYnJlYWtzdHlsZTogJ2JlZm9yZSdcbiAgfSk7XG4gIHJldHVybiBNbWxNc3R5bGU7XG59KE1tbE5vZGVfanNfMS5BYnN0cmFjdE1tbExheW91dE5vZGUpO1xuZXhwb3J0cy5NbWxNc3R5bGUgPSBNbWxNc3R5bGU7IiwiXCJ1c2Ugc3RyaWN0XCI7XG5cbnZhciBfX2V4dGVuZHMgPSB0aGlzICYmIHRoaXMuX19leHRlbmRzIHx8IGZ1bmN0aW9uICgpIHtcbiAgdmFyIGV4dGVuZFN0YXRpY3MgPSBmdW5jdGlvbiAoZCwgYikge1xuICAgIGV4dGVuZFN0YXRpY3MgPSBPYmplY3Quc2V0UHJvdG90eXBlT2YgfHwge1xuICAgICAgX19wcm90b19fOiBbXVxuICAgIH0gaW5zdGFuY2VvZiBBcnJheSAmJiBmdW5jdGlvbiAoZCwgYikge1xuICAgICAgZC5fX3Byb3RvX18gPSBiO1xuICAgIH0gfHwgZnVuY3Rpb24gKGQsIGIpIHtcbiAgICAgIGZvciAodmFyIHAgaW4gYikgaWYgKE9iamVjdC5wcm90b3R5cGUuaGFzT3duUHJvcGVydHkuY2FsbChiLCBwKSkgZFtwXSA9IGJbcF07XG4gICAgfTtcbiAgICByZXR1cm4gZXh0ZW5kU3RhdGljcyhkLCBiKTtcbiAgfTtcbiAgcmV0dXJuIGZ1bmN0aW9uIChkLCBiKSB7XG4gICAgaWYgKHR5cGVvZiBiICE9PSBcImZ1bmN0aW9uXCIgJiYgYiAhPT0gbnVsbCkgdGhyb3cgbmV3IFR5cGVFcnJvcihcIkNsYXNzIGV4dGVuZHMgdmFsdWUgXCIgKyBTdHJpbmcoYikgKyBcIiBpcyBub3QgYSBjb25zdHJ1Y3RvciBvciBudWxsXCIpO1xuICAgIGV4dGVuZFN0YXRpY3MoZCwgYik7XG4gICAgZnVuY3Rpb24gX18oKSB7XG4gICAgICB0aGlzLmNvbnN0cnVjdG9yID0gZDtcbiAgICB9XG4gICAgZC5wcm90b3R5cGUgPSBiID09PSBudWxsID8gT2JqZWN0LmNyZWF0ZShiKSA6IChfXy5wcm90b3R5cGUgPSBiLnByb3RvdHlwZSwgbmV3IF9fKCkpO1xuICB9O1xufSgpO1xuT2JqZWN0LmRlZmluZVByb3BlcnR5KGV4cG9ydHMsIFwiX19lc01vZHVsZVwiLCB7XG4gIHZhbHVlOiB0cnVlXG59KTtcbmV4cG9ydHMuQWJzdHJhY3ROb2RlRmFjdG9yeSA9IHZvaWQgMDtcbnZhciBGYWN0b3J5X2pzXzEgPSByZXF1aXJlKFwiLi9GYWN0b3J5LmpzXCIpO1xudmFyIEFic3RyYWN0Tm9kZUZhY3RvcnkgPSBmdW5jdGlvbiAoX3N1cGVyKSB7XG4gIF9fZXh0ZW5kcyhBYnN0cmFjdE5vZGVGYWN0b3J5LCBfc3VwZXIpO1xuICBmdW5jdGlvbiBBYnN0cmFjdE5vZGVGYWN0b3J5KCkge1xuICAgIHJldHVybiBfc3VwZXIgIT09IG51bGwgJiYgX3N1cGVyLmFwcGx5KHRoaXMsIGFyZ3VtZW50cykgfHwgdGhpcztcbiAgfVxuICBBYnN0cmFjdE5vZGVGYWN0b3J5LnByb3RvdHlwZS5jcmVhdGUgPSBmdW5jdGlvbiAoa2luZCwgcHJvcGVydGllcywgY2hpbGRyZW4pIHtcbiAgICBpZiAocHJvcGVydGllcyA9PT0gdm9pZCAwKSB7XG4gICAgICBwcm9wZXJ0aWVzID0ge307XG4gICAgfVxuICAgIGlmIChjaGlsZHJlbiA9PT0gdm9pZCAwKSB7XG4gICAgICBjaGlsZHJlbiA9IFtdO1xuICAgIH1cbiAgICByZXR1cm4gdGhpcy5ub2RlW2tpbmRdKHByb3BlcnRpZXMsIGNoaWxkcmVuKTtcbiAgfTtcbiAgcmV0dXJuIEFic3RyYWN0Tm9kZUZhY3Rvcnk7XG59KEZhY3RvcnlfanNfMS5BYnN0cmFjdEZhY3RvcnkpO1xuZXhwb3J0cy5BYnN0cmFjdE5vZGVGYWN0b3J5ID0gQWJzdHJhY3ROb2RlRmFjdG9yeTsiXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=
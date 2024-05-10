"use strict";
(self["webpackChunkjupyterlab_more_shortcuts"] = self["webpackChunkjupyterlab_more_shortcuts"] || []).push([["lib_index_js-webpack_sharing_consume_default_codemirror_language-webpack_sharing_consume_defa-b936d0"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _codemirror_commands__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @codemirror/commands */ "./node_modules/@codemirror/commands/dist/index.js");
/* harmony import */ var _codemirror_search__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @codemirror/search */ "./node_modules/@codemirror/search/dist/index.js");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);



/**
 * Initialization data for the jupyterlab_more_shortcuts extension.
 */
const plugin = {
    id: 'jupyterlab_more_shortcuts:plugin',
    description: 'Bring more Codemirror shortcuts to jupyterlab settings.',
    autoStart: true,
    requires: [_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.INotebookTracker],
    // activate: (app: JupyterFrontEnd) => {
    activate: (app, tracker) => {
        console.log('JupyterLab extension jupyterlab_more_shortcuts is activated!');
        var stack = [];
        app.commands.addCommand('codemirror:selectSelectionMatches', {
            execute: () => {
                var _a;
                const cEditor = (_a = tracker.activeCell) === null || _a === void 0 ? void 0 : _a.editor;
                var sel = cEditor.getSelections();
                stack.push(sel);
                if (sel.length == 1 && sel[0].start.column == sel[0].end.column)
                    cEditor.execCommand(_codemirror_search__WEBPACK_IMPORTED_MODULE_1__.selectNextOccurrence);
                cEditor.execCommand(_codemirror_search__WEBPACK_IMPORTED_MODULE_1__.selectSelectionMatches);
            }
        });
        var aa = {
            'selectLine': _codemirror_commands__WEBPACK_IMPORTED_MODULE_2__.selectLine,
            // 'selectSelectionMatches': selectSelectionMatches,
            'selectNextOccurrence': _codemirror_search__WEBPACK_IMPORTED_MODULE_1__.selectNextOccurrence,
            // 'cursorMatchingBracket': f.cursorMatchingBracket,
            // 'selectMatchingBracket': f.selectMatchingBracket,
            'cursorSyntaxLeft': _codemirror_commands__WEBPACK_IMPORTED_MODULE_2__.cursorSyntaxLeft,
            'cursorSyntaxRight': _codemirror_commands__WEBPACK_IMPORTED_MODULE_2__.cursorSyntaxRight,
            'selectSyntaxLeft': _codemirror_commands__WEBPACK_IMPORTED_MODULE_2__.selectSyntaxLeft,
            'selectSyntaxRight': _codemirror_commands__WEBPACK_IMPORTED_MODULE_2__.selectSyntaxRight,
            'cursorSubwordBackward': _codemirror_commands__WEBPACK_IMPORTED_MODULE_2__.cursorSubwordBackward,
            'cursorSubwordForward': _codemirror_commands__WEBPACK_IMPORTED_MODULE_2__.cursorSubwordForward,
            'selectSubwordBackward': _codemirror_commands__WEBPACK_IMPORTED_MODULE_2__.selectSubwordBackward,
            'selectSubwordForward': _codemirror_commands__WEBPACK_IMPORTED_MODULE_2__.selectSubwordForward,
            'selectParentSyntax': _codemirror_commands__WEBPACK_IMPORTED_MODULE_2__.selectParentSyntax,
            'deleteToLineStart': _codemirror_commands__WEBPACK_IMPORTED_MODULE_2__.deleteToLineStart,
            'deleteToLineEnd': _codemirror_commands__WEBPACK_IMPORTED_MODULE_2__.deleteToLineEnd,
            'insertNewlineAndIndent': _codemirror_commands__WEBPACK_IMPORTED_MODULE_2__.insertNewlineAndIndent,
            'insertBlankLine': _codemirror_commands__WEBPACK_IMPORTED_MODULE_2__.insertBlankLine,
        };
        for (let i in aa) {
            app.commands.addCommand('codemirror:' + i, {
                execute: () => {
                    var _a;
                    const cEditor = (_a = tracker.activeCell) === null || _a === void 0 ? void 0 : _a.editor;
                    stack.push(cEditor.getSelections());
                    cEditor.execCommand(aa[i]);
                }
            });
        }
        app.commands.addCommand('codemirror:add-cursor-up', {
            execute: () => {
                var _a;
                const cEditor = (_a = tracker.activeCell) === null || _a === void 0 ? void 0 : _a.editor;
                var a = cEditor.getSelections();
                var b = a.at(0);
                if (!b)
                    return;
                var x = cEditor.getLine(b.end.line - 1);
                var bec = (!x || (x === null || x === void 0 ? void 0 : x.length) >= b.end.column) ? b.end.column : x === null || x === void 0 ? void 0 : x.length;
                var bsc = (!x || (x === null || x === void 0 ? void 0 : x.length) >= b.start.column) ? b.start.column : x === null || x === void 0 ? void 0 : x.length;
                var c = [{ end: { column: bec, line: b.end.line - 1 }, start: { column: bsc, line: b.start.line - 1 } }];
                cEditor.setSelections(c.concat(a));
            }
        });
        app.commands.addCommand('codemirror:add-cursor-down', {
            execute: () => {
                var _a;
                const cEditor = (_a = tracker.activeCell) === null || _a === void 0 ? void 0 : _a.editor;
                var a = cEditor.getSelections();
                var b = a.at(-1);
                if (!b)
                    return;
                var x = cEditor.getLine(b.end.line + 1);
                var bec = (!x || (x === null || x === void 0 ? void 0 : x.length) >= b.end.column) ? b.end.column : x === null || x === void 0 ? void 0 : x.length;
                var bsc = (!x || (x === null || x === void 0 ? void 0 : x.length) >= b.start.column) ? b.start.column : x === null || x === void 0 ? void 0 : x.length;
                var c = [{ end: { column: bec, line: b.end.line + 1 }, start: { column: bsc, line: b.start.line + 1 } }];
                cEditor.setSelections(c.concat(a));
            }
        });
        app.commands.addCommand('codemirror:add-cursor-for-each-line', {
            execute: () => {
                var _a;
                const cEditor = (_a = tracker.activeCell) === null || _a === void 0 ? void 0 : _a.editor;
                var a = cEditor.getSelection();
                var c = [];
                for (let i = a.start.line; i <= a.end.line; i++)
                    c.push({ end: { column: 0, line: i }, start: { column: 0, line: i } });
                cEditor.setSelections(c);
                cEditor.execCommand(_codemirror_commands__WEBPACK_IMPORTED_MODULE_2__.selectLineBoundaryForward);
            }
        });
        // // wtf1: string
        app.commands.addCommand('codemirror:cursorMatchingBracket', {
            execute: () => {
                var _a;
                const cEditor = (_a = tracker.activeCell) === null || _a === void 0 ? void 0 : _a.editor;
                let wtf = cEditor.doc;
                let sel = cEditor.getSelection();
                let offset = cEditor.getOffsetAt(sel.start);
                var a = wtf.sliceString(offset, offset + 1);
                if (a == ')' || a == ']' || a == '}')
                    cEditor.execCommand(_codemirror_commands__WEBPACK_IMPORTED_MODULE_2__.cursorMatchingBracket);
                else {
                    var hit = 1;
                    while (offset >= 1) {
                        var a = wtf.sliceString(offset - 1, offset);
                        if (a == '(' || a == '[' || a == '{')
                            hit -= 1;
                        else if (a == ')' || a == ']' || a == '}')
                            hit += 1;
                        if (hit == 0)
                            break;
                        offset -= 1;
                        cEditor.execCommand(_codemirror_commands__WEBPACK_IMPORTED_MODULE_2__.cursorCharLeft);
                    }
                    cEditor.execCommand(_codemirror_commands__WEBPACK_IMPORTED_MODULE_2__.cursorMatchingBracket);
                }
            }
        });
        app.commands.addCommand('codemirror:selectMatchingBracket', {
            execute: () => {
                var _a;
                const cEditor = (_a = tracker.activeCell) === null || _a === void 0 ? void 0 : _a.editor;
                let doc = cEditor.doc;
                let sel = cEditor.getSelection();
                stack.push([sel]);
                let offset = cEditor.getOffsetAt(sel.start);
                if (sel.start.column != sel.end.column && offset >= 1)
                    offset -= 1;
                var hit = 1;
                while (offset >= 1) {
                    var a = doc.sliceString(offset - 1, offset);
                    if (a == '(' || a == '[' || a == '{')
                        hit -= 1;
                    else if (a == ')' || a == ']' || a == '}')
                        hit += 1;
                    if (hit == 0)
                        break;
                    offset -= 1;
                }
                cEditor.setCursorPosition(cEditor.getPositionAt(offset));
                cEditor.execCommand(_codemirror_commands__WEBPACK_IMPORTED_MODULE_2__.selectMatchingBracket);
            }
        });
        app.commands.addCommand('codemirror:selectString', {
            execute: () => {
                var _a;
                const cEditor = (_a = tracker.activeCell) === null || _a === void 0 ? void 0 : _a.editor;
                let doc = cEditor.doc;
                let sel = cEditor.getSelection();
                stack.push([sel]);
                let offset = cEditor.getOffsetAt(sel.start);
                while (offset >= 1) {
                    var a = doc.sliceString(offset - 1, offset);
                    if (a == '"' || a == "'")
                        break;
                    offset -= 1;
                }
                let offset2 = cEditor.getOffsetAt(sel.start) + 1;
                while (offset2 < doc.length) {
                    var a = doc.sliceString(offset2 - 1, offset2);
                    if (a == '"' || a == "'")
                        break;
                    offset2 += 1;
                }
                cEditor.setSelections([{ start: cEditor.getPositionAt(offset), end: cEditor.getPositionAt(offset2 - 1) }]);
            }
        });
        // wtf: undo bracket selection
        // TODO: add another redo stack
        app.commands.addCommand('codemirror:undoSelection', {
            execute: () => {
                var _a;
                const cEditor = (_a = tracker.activeCell) === null || _a === void 0 ? void 0 : _a.editor;
                // while (true) {
                var poped = stack.pop();
                if (!poped)
                    return;
                // var cur = cEditor.getSelections()
                // if (cur.length!=poped.length )
                // if (poped.start.column != cur.start.column || poped.end.column != cur.end.column) {
                cEditor.setSelections(poped);
                // break
                // }
                // }
            }
        });
        app.commands.addCommand('codemirror:deleteSubwordLeft', {
            execute: () => {
                var _a;
                const cEditor = (_a = tracker.activeCell) === null || _a === void 0 ? void 0 : _a.editor;
                cEditor.execCommand(_codemirror_commands__WEBPACK_IMPORTED_MODULE_2__.selectSubwordBackward);
                cEditor.execCommand(_codemirror_commands__WEBPACK_IMPORTED_MODULE_2__.deleteCharBackward);
            }
        });
        app.commands.addCommand('codemirror:deleteSubwordRight', {
            execute: () => {
                var _a;
                const cEditor = (_a = tracker.activeCell) === null || _a === void 0 ? void 0 : _a.editor;
                cEditor.execCommand(_codemirror_commands__WEBPACK_IMPORTED_MODULE_2__.selectSubwordForward);
                cEditor.execCommand(_codemirror_commands__WEBPACK_IMPORTED_MODULE_2__.deleteCharBackward);
            }
        });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ })

}]);
//# sourceMappingURL=lib_index_js-webpack_sharing_consume_default_codemirror_language-webpack_sharing_consume_defa-b936d0.66d6006fc751f5f66c71.js.map
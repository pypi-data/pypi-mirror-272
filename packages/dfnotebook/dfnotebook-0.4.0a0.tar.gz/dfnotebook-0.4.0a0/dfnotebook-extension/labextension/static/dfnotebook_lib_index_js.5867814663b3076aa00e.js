"use strict";
(self["webpackChunk_dfnotebook_dfnotebook_extension"] = self["webpackChunk_dfnotebook_dfnotebook_extension"] || []).push([["dfnotebook_lib_index_js"],{

/***/ "../dfnotebook/lib/actions.js":
/*!************************************!*\
  !*** ../dfnotebook/lib/actions.js ***!
  \************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "DataflowNotebookActions": () => (/* binding */ DataflowNotebookActions)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_domutils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/domutils */ "webpack/sharing/consume/default/@lumino/domutils");
/* harmony import */ var _lumino_domutils__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_domutils__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _dfnotebook_dfcells__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @dfnotebook/dfcells */ "webpack/sharing/consume/default/@dfnotebook/dfcells/@dfnotebook/dfcells");
/* harmony import */ var _dfnotebook_dfcells__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_dfnotebook_dfcells__WEBPACK_IMPORTED_MODULE_6__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.







/**
 * A collection of actions that run against notebooks.
 *
 * #### Notes
 * All of the actions are a no-op if there is no model on the notebook.
 * The actions set the widget `mode` to `'command'` unless otherwise specified.
 * The actions will preserve the selection on the notebook widget unless
 * otherwise specified.
 */
class DataflowNotebookActions {
    /**
     * A signal that emits whenever a cell completes execution.
     */
    static get executed() {
        return Private.executed;
    }
    /**
     * A signal that emits whenever a cell execution is scheduled.
     */
    static get executionScheduled() {
        return Private.executionScheduled;
    }
    /**
     * A signal that emits whenever a cell execution is scheduled.
     */
    static get selectionExecuted() {
        return Private.selectionExecuted;
    }
    /**
     * A private constructor for the `NotebookActions` class.
     *
     * #### Notes
     * This class can never be instantiated. Its static member `executed` will be
     * merged with the `NotebookActions` namespace. The reason it exists as a
     * standalone class is because at run time, the `Private.executed` variable
     * does not yet exist, so it needs to be referenced via a getter.
     */
    constructor() {
        // Intentionally empty.
    }
}
/**
 * A namespace for `NotebookActions` static methods.
 */
(function (DataflowNotebookActions) {
    /**
     * Run the selected cell(s).
     *
     * @param notebook - The target notebook widget.
     *
     * @param sessionContext - The optional client session object.
     *
     * #### Notes
     * The last selected cell will be activated, but not scrolled into view.
     * The existing selection will be cleared.
     * An execution error will prevent the remaining code cells from executing.
     * All markdown cells will be rendered.
     */
    function run(notebook, sessionContext) {
        if (!notebook.model || !notebook.activeCell) {
            return Promise.resolve(false);
        }
        const state = Private.getState(notebook);
        const promise = Private.runSelected(notebook, sessionContext);
        Private.handleRunState(notebook, state, false);
        return promise;
    }
    DataflowNotebookActions.run = run;
    /**
     * Run the selected cell(s) and advance to the next cell.
     *
     * @param notebook - The target notebook widget.
     *
     * @param sessionContext - The optional client session object.
     *
     * #### Notes
     * The existing selection will be cleared.
     * The cell after the last selected cell will be activated and scrolled into view.
     * An execution error will prevent the remaining code cells from executing.
     * All markdown cells will be rendered.
     * If the last selected cell is the last cell, a new code cell
     * will be created in `'edit'` mode.  The new cell creation can be undone.
     */
    function runAndAdvance(notebook, sessionContext) {
        if (!notebook.model || !notebook.activeCell) {
            return Promise.resolve(false);
        }
        const state = Private.getState(notebook);
        const promise = Private.runSelected(notebook, sessionContext);
        const model = notebook.model;
        if (notebook.activeCellIndex === notebook.widgets.length - 1) {
            const cell = model.contentFactory.createCell(notebook.notebookConfig.defaultCell, {});
            // Do not use push here, as we want an widget insertion
            // to make sure no placeholder widget is rendered.
            model.cells.insert(notebook.widgets.length, cell);
            notebook.activeCellIndex++;
            notebook.mode = 'edit';
        }
        else {
            notebook.activeCellIndex++;
        }
        Private.handleRunState(notebook, state, true);
        return promise;
    }
    DataflowNotebookActions.runAndAdvance = runAndAdvance;
    /**
     * Run the selected cell(s) and insert a new code cell.
     *
     * @param notebook - The target notebook widget.
     *
     * @param sessionContext - The optional client session object.
     *
     * #### Notes
     * An execution error will prevent the remaining code cells from executing.
     * All markdown cells will be rendered.
     * The widget mode will be set to `'edit'` after running.
     * The existing selection will be cleared.
     * The cell insert can be undone.
     * The new cell will be scrolled into view.
     */
    function runAndInsert(notebook, sessionContext) {
        if (!notebook.model || !notebook.activeCell) {
            return Promise.resolve(false);
        }
        if (!Private.isNotebookRendered(notebook)) {
            return Promise.resolve(false);
        }
        const state = Private.getState(notebook);
        const promise = Private.runSelected(notebook, sessionContext);
        const model = notebook.model;
        const cell = model.contentFactory.createCell(notebook.notebookConfig.defaultCell, {});
        model.cells.insert(notebook.activeCellIndex + 1, cell);
        notebook.activeCellIndex++;
        notebook.mode = 'edit';
        Private.handleRunState(notebook, state, true);
        return promise;
    }
    DataflowNotebookActions.runAndInsert = runAndInsert;
    /**
     * Run all of the cells in the notebook.
     *
     * @param notebook - The target notebook widget.
     *
     * @param sessionContext - The optional client session object.
     *
     * #### Notes
     * The existing selection will be cleared.
     * An execution error will prevent the remaining code cells from executing.
     * All markdown cells will be rendered.
     * The last cell in the notebook will be activated and scrolled into view.
     */
    function runAll(notebook, sessionContext) {
        if (!notebook.model || !notebook.activeCell) {
            return Promise.resolve(false);
        }
        const state = Private.getState(notebook);
        notebook.widgets.forEach(child => {
            notebook.select(child);
        });
        const promise = Private.runSelected(notebook, sessionContext);
        Private.handleRunState(notebook, state, true);
        return promise;
    }
    DataflowNotebookActions.runAll = runAll;
    function renderAllMarkdown(notebook, sessionContext) {
        if (!notebook.model || !notebook.activeCell) {
            return Promise.resolve(false);
        }
        const previousIndex = notebook.activeCellIndex;
        const state = Private.getState(notebook);
        notebook.widgets.forEach((child, index) => {
            if (child.model.type === 'markdown') {
                notebook.select(child);
                // This is to make sure that the activeCell
                // does not get executed
                notebook.activeCellIndex = index;
            }
        });
        if (notebook.activeCell.model.type !== 'markdown') {
            return Promise.resolve(true);
        }
        const promise = Private.runSelected(notebook, sessionContext);
        notebook.activeCellIndex = previousIndex;
        Private.handleRunState(notebook, state, true);
        return promise;
    }
    DataflowNotebookActions.renderAllMarkdown = renderAllMarkdown;
    /**
     * Run all of the cells before the currently active cell (exclusive).
     *
     * @param notebook - The target notebook widget.
     *
     * @param sessionContext - The optional client session object.
     *
     * #### Notes
     * The existing selection will be cleared.
     * An execution error will prevent the remaining code cells from executing.
     * All markdown cells will be rendered.
     * The currently active cell will remain selected.
     */
    function runAllAbove(notebook, sessionContext) {
        const { activeCell, activeCellIndex, model } = notebook;
        if (!model || !activeCell || activeCellIndex < 1) {
            return Promise.resolve(false);
        }
        const state = Private.getState(notebook);
        notebook.activeCellIndex--;
        notebook.deselectAll();
        for (let i = 0; i < notebook.activeCellIndex; ++i) {
            notebook.select(notebook.widgets[i]);
        }
        const promise = Private.runSelected(notebook, sessionContext);
        notebook.activeCellIndex++;
        Private.handleRunState(notebook, state, true);
        return promise;
    }
    DataflowNotebookActions.runAllAbove = runAllAbove;
    /**
     * Run all of the cells after the currently active cell (inclusive).
     *
     * @param notebook - The target notebook widget.
     *
     * @param sessionContext - The optional client session object.
     *
     * #### Notes
     * The existing selection will be cleared.
     * An execution error will prevent the remaining code cells from executing.
     * All markdown cells will be rendered.
     * The last cell in the notebook will be activated and scrolled into view.
     */
    function runAllBelow(notebook, sessionContext) {
        if (!notebook.model || !notebook.activeCell) {
            return Promise.resolve(false);
        }
        const state = Private.getState(notebook);
        notebook.deselectAll();
        for (let i = notebook.activeCellIndex; i < notebook.widgets.length; ++i) {
            notebook.select(notebook.widgets[i]);
        }
        const promise = Private.runSelected(notebook, sessionContext);
        Private.handleRunState(notebook, state, true);
        return promise;
    }
    DataflowNotebookActions.runAllBelow = runAllBelow;
})(DataflowNotebookActions || (DataflowNotebookActions = {}));
/**
 * A namespace for private data.
 */
var Private;
(function (Private) {
    /**
     * A signal that emits whenever a cell completes execution.
     */
    Private.executed = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_4__.Signal({});
    /**
     * A signal that emits whenever a cell execution is scheduled.
     */
    Private.executionScheduled = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_4__.Signal({});
    /**
     * A signal that emits when one notebook's cells are all executed.
     */
    Private.selectionExecuted = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_4__.Signal({});
    function isNotebookRendered(notebook) {
        const translator = notebook.translator;
        const trans = translator.load('jupyterlab');
        if (notebook.remainingCellToRenderCount !== 0) {
            (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({
                body: trans.__(`Notebook is still rendering and has for now (%1) remaining cells to render.

Please wait for the complete rendering before invoking that action.`, notebook.remainingCellToRenderCount),
                buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.okButton({ label: trans.__('Ok') })]
            }).catch(reason => {
                console.error('An error occurred when displaying notebook rendering warning', reason);
            });
            return false;
        }
        return true;
    }
    Private.isNotebookRendered = isNotebookRendered;
    /**
     * Get the state of a widget before running an action.
     */
    function getState(notebook) {
        return {
            wasFocused: notebook.node.contains(document.activeElement),
            activeCell: notebook.activeCell
        };
    }
    Private.getState = getState;
    /**
     * Handle the state of a widget after running an action.
     */
    function handleState(notebook, state, scrollIfNeeded = false) {
        const { activeCell, node } = notebook;
        if (state.wasFocused || notebook.mode === 'edit') {
            notebook.activate();
        }
        if (scrollIfNeeded && activeCell) {
            _lumino_domutils__WEBPACK_IMPORTED_MODULE_3__.ElementExt.scrollIntoViewIfNeeded(node, activeCell.node);
        }
    }
    Private.handleState = handleState;
    /**
     * Handle the state of a widget after running a run action.
     */
    function handleRunState(notebook, state, scroll = false) {
        if (state.wasFocused || notebook.mode === 'edit') {
            notebook.activate();
        }
        if (scroll && state.activeCell) {
            // Scroll to the top of the previous active cell output.
            const rect = state.activeCell.inputArea.node.getBoundingClientRect();
            notebook.scrollToPosition(rect.bottom, 45);
        }
    }
    Private.handleRunState = handleRunState;
    /**
     * Run the selected cells.
     */
    function runSelected(notebook, sessionContext) {
        notebook.mode = 'command';
        let lastIndex = notebook.activeCellIndex;
        const selected = notebook.widgets.filter((child, index) => {
            const active = notebook.isSelectedOrActive(child);
            if (active) {
                lastIndex = index;
            }
            return active;
        });
        notebook.activeCellIndex = lastIndex;
        notebook.deselectAll();
        return Promise.all(selected.map(child => runCell(notebook, child, sessionContext)))
            .then(results => {
            if (notebook.isDisposed) {
                return false;
            }
            Private.selectionExecuted.emit({
                notebook,
                lastCell: notebook.widgets[lastIndex]
            });
            // Post an update request.
            notebook.update();
            return results.every(result => result);
        })
            .catch(reason => {
            if (reason.message.startsWith('KernelReplyNotOK')) {
                selected.map(cell => {
                    // Remove '*' prompt from cells that didn't execute
                    if (cell.model.type === 'code' &&
                        cell.model.executionCount == null) {
                        cell.setPrompt('');
                    }
                });
            }
            else {
                throw reason;
            }
            Private.selectionExecuted.emit({
                notebook,
                lastCell: notebook.widgets[lastIndex]
            });
            notebook.update();
            return false;
        });
    }
    Private.runSelected = runSelected;
    /**
     * Run a cell.
     */
    function runCell(notebook, cell, sessionContext, translator) {
        var _a, _b, _c;
        translator = translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__.nullTranslator;
        const trans = translator.load('jupyterlab');
        switch (cell.model.type) {
            case 'markdown':
                cell.rendered = true;
                cell.inputHidden = false;
                Private.executed.emit({ notebook, cell, success: true });
                break;
            case 'code':
                if (sessionContext) {
                    if (sessionContext.isTerminating) {
                        void (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({
                            title: trans.__('Kernel Terminating'),
                            body: trans.__('The kernel for %1 appears to be terminating. You can not run any cell for now.', (_a = sessionContext.session) === null || _a === void 0 ? void 0 : _a.path),
                            buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.okButton({ label: trans.__('Ok') })]
                        });
                        break;
                    }
                    if (sessionContext.pendingInput) {
                        void (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({
                            title: trans.__('Cell not executed due to pending input'),
                            body: trans.__('The cell has not been executed to avoid kernel deadlock as there is another pending input! Submit your pending input and try again.'),
                            buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.okButton({ label: trans.__('Ok') })]
                        });
                        return Promise.resolve(false);
                    }
                    if (sessionContext.hasNoKernel) {
                        void _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.sessionContextDialogs.selectKernel(sessionContext);
                        return Promise.resolve(false);
                    }
                    const deletedCells = (_c = (_b = notebook.model) === null || _b === void 0 ? void 0 : _b.deletedCells) !== null && _c !== void 0 ? _c : [];
                    const codeDict = {};
                    const cellIdWidgetMap = {};
                    const outputTags = {};
                    const inputTags = {};
                    if (notebook.model) {
                        (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_2__.each)(notebook.model.cells, (c, index) => {
                            const child = notebook.widgets[index];
                            if (c.type === 'code') {
                                // FIXME replace with utility function (see dfcells/widget)
                                const cId = c.id.replace(/-/g, '').substring(0, 8);
                                const inputTag = c.metadata.get('tag');
                                if (inputTag) {
                                    // FIXME need to check for duplicates!
                                    inputTags[inputTag] = cId;
                                }
                                codeDict[cId] = c.value.text;
                                cellIdWidgetMap[cId] = child;
                                let cellOutputTags = [];
                                for (let i = 0; i < child.outputArea.model.length; ++i) {
                                    const out = child.outputArea.model.get(i);
                                    if (out.metadata['output_tag']) {
                                        cellOutputTags.push(out.metadata['output_tag']);
                                    }
                                }
                                outputTags[cId] = cellOutputTags;
                            }
                        });
                    }
                    // console.log('codeDict:', codeDict);
                    // console.log('cellIdWidgetMap:', cellIdWidgetMap);
                    // console.log('outputTags:', outputTags);
                    // console.log('inputTags:', inputTags);
                    const dfData = {
                        // FIXME replace with utility function (see dfcells/widget)
                        uuid: cell.model.id.replace(/-/g, '').substring(0, 8) || '',
                        code_dict: codeDict,
                        output_tags: outputTags,
                        input_tags: inputTags,
                        auto_update_flags: {},
                        force_cached_flags: {} // this.notebook.get_force_cached_flags()})
                    };
                    Private.executionScheduled.emit({ notebook, cell });
                    return _dfnotebook_dfcells__WEBPACK_IMPORTED_MODULE_6__.DataflowCodeCell.execute(cell, sessionContext, {
                        deletedCells,
                        recordTiming: notebook.notebookConfig.recordTiming,
                    }, dfData, cellIdWidgetMap)
                        .then(reply => {
                        deletedCells.splice(0, deletedCells.length);
                        if (cell.isDisposed) {
                            return false;
                        }
                        if (!reply) {
                            return true;
                        }
                        if (reply.content.status === 'ok') {
                            const content = reply.content;
                            if (content.payload && content.payload.length) {
                                handlePayload(content, notebook, cell);
                            }
                            return true;
                        }
                        else {
                            throw new _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_5__.KernelError(reply.content);
                        }
                    })
                        .catch(reason => {
                        if (cell.isDisposed || reason.message.startsWith('Canceled')) {
                            return false;
                        }
                        Private.executed.emit({ notebook, cell, success: false, error: reason });
                        throw reason;
                    })
                        .then(ran => {
                        if (ran) {
                            Private.executed.emit({ notebook, cell, success: true });
                        }
                        return ran;
                    });
                }
                cell.model.clearExecution();
                break;
            default:
                break;
        }
        return Promise.resolve(true);
    }
    /**
     * Handle payloads from an execute reply.
     *
     * #### Notes
     * Payloads are deprecated and there are no official interfaces for them in
     * the kernel type definitions.
     * See [Payloads (DEPRECATED)](https://jupyter-client.readthedocs.io/en/latest/messaging.html#payloads-deprecated).
     */
    function handlePayload(content, notebook, cell) {
        var _a;
        const setNextInput = (_a = content.payload) === null || _a === void 0 ? void 0 : _a.filter(i => {
            return i.source === 'set_next_input';
        })[0];
        if (!setNextInput) {
            return;
        }
        const text = setNextInput.text;
        const replace = setNextInput.replace;
        if (replace) {
            cell.model.value.text = text;
            return;
        }
        // Create a new code cell and add as the next cell.
        const newCell = notebook.model.contentFactory.createCodeCell({});
        const cells = notebook.model.cells;
        const index = _lumino_algorithm__WEBPACK_IMPORTED_MODULE_2__.ArrayExt.firstIndexOf((0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_2__.toArray)(cells), cell.model);
        newCell.value.text = text;
        if (index === -1) {
            cells.push(newCell);
        }
        else {
            cells.insert(index + 1, newCell);
        }
    }
    /**
     * Get the selected cell(s) without affecting the clipboard.
     *
     * @param notebook - The target notebook widget.
     *
     * @returns A list of 0 or more selected cells
     */
    function selectedCells(notebook) {
        return notebook.widgets
            .filter(cell => notebook.isSelectedOrActive(cell))
            .map(cell => cell.model.toJSON())
            .map(cellJSON => {
            if (cellJSON.metadata.deletable !== undefined) {
                delete cellJSON.metadata.deletable;
            }
            return cellJSON;
        });
    }
    Private.selectedCells = selectedCells;
})(Private || (Private = {}));
//# sourceMappingURL=actions.js.map

/***/ }),

/***/ "../dfnotebook/lib/index.js":
/*!**********************************!*\
  !*** ../dfnotebook/lib/index.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "DataflowNotebook": () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_4__.DataflowNotebook),
/* harmony export */   "DataflowNotebookActions": () => (/* reexport safe */ _actions__WEBPACK_IMPORTED_MODULE_0__.DataflowNotebookActions),
/* harmony export */   "DataflowNotebookModel": () => (/* reexport safe */ _model__WEBPACK_IMPORTED_MODULE_1__.DataflowNotebookModel),
/* harmony export */   "DataflowNotebookModelFactory": () => (/* reexport safe */ _modelfactory__WEBPACK_IMPORTED_MODULE_2__.DataflowNotebookModelFactory),
/* harmony export */   "DataflowNotebookPanel": () => (/* reexport safe */ _panel__WEBPACK_IMPORTED_MODULE_3__.DataflowNotebookPanel),
/* harmony export */   "DataflowNotebookWidgetFactory": () => (/* reexport safe */ _widgetfactory__WEBPACK_IMPORTED_MODULE_6__.DataflowNotebookWidgetFactory),
/* harmony export */   "DataflowStaticNotebook": () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_4__.DataflowStaticNotebook),
/* harmony export */   "IDataflowNotebookContentFactory": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_5__.IDataflowNotebookContentFactory),
/* harmony export */   "IDataflowNotebookModelFactory": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_5__.IDataflowNotebookModelFactory),
/* harmony export */   "IDataflowNotebookWidgetFactory": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_5__.IDataflowNotebookWidgetFactory)
/* harmony export */ });
/* harmony import */ var _actions__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./actions */ "../dfnotebook/lib/actions.js");
/* harmony import */ var _model__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./model */ "../dfnotebook/lib/model.js");
/* harmony import */ var _modelfactory__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./modelfactory */ "../dfnotebook/lib/modelfactory.js");
/* harmony import */ var _panel__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./panel */ "../dfnotebook/lib/panel.js");
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./widget */ "../dfnotebook/lib/widget.js");
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./tokens */ "../dfnotebook/lib/tokens.js");
/* harmony import */ var _widgetfactory__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./widgetfactory */ "../dfnotebook/lib/widgetfactory.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module dfnotebook
 */







//# sourceMappingURL=index.js.map

/***/ }),

/***/ "../dfnotebook/lib/model.js":
/*!**********************************!*\
  !*** ../dfnotebook/lib/model.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "DataflowNotebookModel": () => (/* binding */ DataflowNotebookModel)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _dfnotebook_dfcells__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @dfnotebook/dfcells */ "webpack/sharing/consume/default/@dfnotebook/dfcells/@dfnotebook/dfcells");
/* harmony import */ var _dfnotebook_dfcells__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_dfnotebook_dfcells__WEBPACK_IMPORTED_MODULE_2__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



class DataflowNotebookModel extends _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.NotebookModel {
    constructor(options = {}) {
        super(Object.assign({ contentFactory: DataflowNotebookModel.defaultContentFactory }, options));
    }
    /**
     * The name of the model.
     */
    get name() {
        return 'dfnotebook';
    }
    fromJSON(value) {
        var _a, _b;
        let isDataflow = true;
        if (((_b = (_a = value.metadata) === null || _a === void 0 ? void 0 : _a.kernelspec) === null || _b === void 0 ? void 0 : _b.name) && value.metadata.kernelspec.name != 'dfpython3') {
            //@ts-expect-error
            this.contentFactory = _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.NotebookModel.defaultContentFactory;
            isDataflow = false;
        }
        super.fromJSON(value);
        this.metadata.set('dfnotebook', isDataflow);
    }
}
/**
 * The namespace for the `NotebookModel` class statics.
 */
(function (DataflowNotebookModel) {
    /**
     * The dataflow implementation of an `IContentFactory`.
     */
    class ContentFactory extends _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.NotebookModel.ContentFactory {
        /*
         * FIXME: Add codeCellContentFactory default to DataflowCodeCellContentFactory??
         */
        constructor(options) {
            super(options);
        }
        /**
         * Create a new code cell.
         *
         * @param source - The data to use for the original source data.
         *
         * @returns A new code cell. If a source cell is provided, the
         *   new cell will be initialized with the data from the source.
         *   If the contentFactory is not provided, the instance
         *   `codeCellContentFactory` will be used.
         */
        createCodeCell(options) {
            if (options.contentFactory) {
                options.contentFactory = this.codeCellContentFactory;
            }
            if (this.modelDB) {
                if (!options.id) {
                    options.id = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.UUID.uuid4();
                }
                options.modelDB = this.modelDB.view(options.id);
            }
            return new _dfnotebook_dfcells__WEBPACK_IMPORTED_MODULE_2__.DataflowCodeCellModel(options);
        }
        /**
         * Create a new markdown cell.
         *
         * @param source - The data to use for the original source data.
         *
         * @returns A new markdown cell. If a source cell is provided, the
         *   new cell will be initialized with the data from the source.
         */
        createMarkdownCell(options) {
            if (this.modelDB) {
                if (!options.id) {
                    options.id = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.UUID.uuid4();
                }
                options.modelDB = this.modelDB.view(options.id);
            }
            return new _dfnotebook_dfcells__WEBPACK_IMPORTED_MODULE_2__.DataflowMarkdownCellModel(options);
        }
        /**
         * Create a new raw cell.
         *
         * @param source - The data to use for the original source data.
         *
         * @returns A new raw cell. If a source cell is provided, the
         *   new cell will be initialized with the data from the source.
         */
        createRawCell(options) {
            if (this.modelDB) {
                if (!options.id) {
                    options.id = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.UUID.uuid4();
                }
                options.modelDB = this.modelDB.view(options.id);
            }
            return new _dfnotebook_dfcells__WEBPACK_IMPORTED_MODULE_2__.DataflowRawCellModel(options);
        }
        /**
         * Clone the content factory with a new IModelDB.
         */
        clone(modelDB) {
            return new ContentFactory({
                modelDB: modelDB,
                codeCellContentFactory: this.codeCellContentFactory
            });
        }
    }
    DataflowNotebookModel.ContentFactory = ContentFactory;
    /**
     * The default `ContentFactory` instance.
     */
    DataflowNotebookModel.defaultContentFactory = new ContentFactory({});
})(DataflowNotebookModel || (DataflowNotebookModel = {}));
//# sourceMappingURL=model.js.map

/***/ }),

/***/ "../dfnotebook/lib/modelfactory.js":
/*!*****************************************!*\
  !*** ../dfnotebook/lib/modelfactory.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "DataflowNotebookModelFactory": () => (/* binding */ DataflowNotebookModelFactory)
/* harmony export */ });
/* harmony import */ var _model__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./model */ "../dfnotebook/lib/model.js");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.


/**
 * A model factory for notebooks.
 */
class DataflowNotebookModelFactory extends _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.NotebookModelFactory {
    /**
     * Construct a new notebook model factory.
     */
    constructor(options) {
        super(Object.assign({ contentFactory: new _model__WEBPACK_IMPORTED_MODULE_1__.DataflowNotebookModel.ContentFactory({
                codeCellContentFactory: options.codeCellContentFactory
            }) }, options));
    }
    /**
     * Create a new model for a given path.
     *
     * @param languagePreference - An optional kernel language preference.
     *
     * @returns A new document model.
     */
    createNew(languagePreference, modelDB, isInitialized) {
        const contentFactory = this.contentFactory;
        return new _model__WEBPACK_IMPORTED_MODULE_1__.DataflowNotebookModel({
            languagePreference,
            contentFactory,
            modelDB,
            isInitialized,
            //@ts-ignore
            disableDocumentWideUndoRedo: this._disableDocumentWideUndoRedo
        });
    }
    /**
     * The name of the model.
     */
    get name() {
        return 'dfnotebook';
    }
}
//# sourceMappingURL=modelfactory.js.map

/***/ }),

/***/ "../dfnotebook/lib/panel.js":
/*!**********************************!*\
  !*** ../dfnotebook/lib/panel.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "DataflowNotebookPanel": () => (/* binding */ DataflowNotebookPanel)
/* harmony export */ });
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./widget */ "../dfnotebook/lib/widget.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * A namespace for `DataflowNotebookPanel` statics.
 */
var DataflowNotebookPanel;
(function (DataflowNotebookPanel) {
    /**
     * The default implementation of an `IContentFactory`.
     */
    class ContentFactory extends _widget__WEBPACK_IMPORTED_MODULE_0__.DataflowNotebook.ContentFactory {
        /**
         * Create a new content area for the panel.
         */
        createNotebook(options) {
            return new _widget__WEBPACK_IMPORTED_MODULE_0__.DataflowNotebook(options);
        }
    }
    DataflowNotebookPanel.ContentFactory = ContentFactory;
    /**
     * Default content factory for the notebook panel.
     */
    DataflowNotebookPanel.defaultContentFactory = new ContentFactory();
})(DataflowNotebookPanel || (DataflowNotebookPanel = {}));
//# sourceMappingURL=panel.js.map

/***/ }),

/***/ "../dfnotebook/lib/tokens.js":
/*!***********************************!*\
  !*** ../dfnotebook/lib/tokens.js ***!
  \***********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IDataflowNotebookContentFactory": () => (/* binding */ IDataflowNotebookContentFactory),
/* harmony export */   "IDataflowNotebookModelFactory": () => (/* binding */ IDataflowNotebookModelFactory),
/* harmony export */   "IDataflowNotebookWidgetFactory": () => (/* binding */ IDataflowNotebookWidgetFactory)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);

/* tslint:disable */
/**
 * The dfnotebook model factory token.
 */
const IDataflowNotebookModelFactory = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@dfnotebook/dfnotebook:IDataflowNotebookModelFactory');
/* tslint:enable */
/* tslint:disable */
/**
 * The dfnotebook widget factory token.
 */
const IDataflowNotebookWidgetFactory = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@dfnotebook/dfnotebook:DataflowNotebookWidgetFactory');
/* tslint:enable */
/* tslint:disable */
/**
 * The dfnotebook content factory token.
 */
const IDataflowNotebookContentFactory = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@dfnotebook/dfnotebook:IDataflowNotebookContentFactory');
/* tslint:enable */ 
//# sourceMappingURL=tokens.js.map

/***/ }),

/***/ "../dfnotebook/lib/widget.js":
/*!***********************************!*\
  !*** ../dfnotebook/lib/widget.js ***!
  \***********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "DataflowNotebook": () => (/* binding */ DataflowNotebook),
/* harmony export */   "DataflowStaticNotebook": () => (/* binding */ DataflowStaticNotebook)
/* harmony export */ });
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/cells */ "webpack/sharing/consume/default/@jupyterlab/cells");
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _dfnotebook_dfcells__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @dfnotebook/dfcells */ "webpack/sharing/consume/default/@dfnotebook/dfcells/@dfnotebook/dfcells");
/* harmony import */ var _dfnotebook_dfcells__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_dfnotebook_dfcells__WEBPACK_IMPORTED_MODULE_2__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



/**
 * The namespace for the `StaticNotebook` class statics.
 */
var DataflowStaticNotebook;
(function (DataflowStaticNotebook) {
    /**
     * The default implementation of an `IContentFactory`.
     */
    class ContentFactory extends _dfnotebook_dfcells__WEBPACK_IMPORTED_MODULE_2__.DataflowCell.ContentFactory {
        /**
         * Create a new code cell widget.
         *
         * #### Notes
         * If no cell content factory is passed in with the options, the one on the
         * notebook content factory is used.
         */
        createCodeCell(options, parent) {
            if (!(options.model instanceof _dfnotebook_dfcells__WEBPACK_IMPORTED_MODULE_2__.DataflowCodeCellModel)) {
                options.contentFactory = _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__.StaticNotebook.defaultContentFactory;
                return new _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__.CodeCell(options).initializeState();
            }
            if (!options.contentFactory) {
                options.contentFactory = this;
            }
            return new _dfnotebook_dfcells__WEBPACK_IMPORTED_MODULE_2__.DataflowCodeCell(options).initializeState();
        }
        /**
         * Create a new markdown cell widget.
         *
         * #### Notes
         * If no cell content factory is passed in with the options, the one on the
         * notebook content factory is used.
         */
        createMarkdownCell(options, parent) {
            if (!(options.model instanceof _dfnotebook_dfcells__WEBPACK_IMPORTED_MODULE_2__.DataflowMarkdownCellModel)) {
                options.contentFactory = _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__.StaticNotebook.defaultContentFactory;
                return new _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__.MarkdownCell(options).initializeState();
            }
            if (!options.contentFactory) {
                options.contentFactory = this;
            }
            return new _dfnotebook_dfcells__WEBPACK_IMPORTED_MODULE_2__.DataflowMarkdownCell(options).initializeState();
        }
        /**
         * Create a new raw cell widget.
         *
         * #### Notes
         * If no cell content factory is passed in with the options, the one on the
         * notebook content factory is used.
         */
        createRawCell(options, parent) {
            if (!(options.model instanceof _dfnotebook_dfcells__WEBPACK_IMPORTED_MODULE_2__.DataflowRawCellModel)) {
                options.contentFactory = _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__.StaticNotebook.defaultContentFactory;
                return new _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__.RawCell(options).initializeState();
            }
            if (!options.contentFactory) {
                options.contentFactory = this;
            }
            return new _dfnotebook_dfcells__WEBPACK_IMPORTED_MODULE_2__.DataflowRawCell(options).initializeState();
        }
    }
    DataflowStaticNotebook.ContentFactory = ContentFactory;
    /**
     * Default content factory for the static notebook widget.
     */
    DataflowStaticNotebook.defaultContentFactory = new ContentFactory();
})(DataflowStaticNotebook || (DataflowStaticNotebook = {}));
class DataflowNotebook extends _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__.Notebook {
    constructor(options) {
        super(Object.assign({ contentFactory: DataflowNotebook.defaultContentFactory }, options));
    }
}
(function (DataflowNotebook) {
    /**
     * The default implementation of a notebook content factory..
     *
     * #### Notes
     * Override methods on this class to customize the default notebook factory
     * methods that create notebook content.
     */
    class ContentFactory extends DataflowStaticNotebook.ContentFactory {
    }
    DataflowNotebook.ContentFactory = ContentFactory;
    DataflowNotebook.defaultContentFactory = new ContentFactory();
})(DataflowNotebook || (DataflowNotebook = {}));
//# sourceMappingURL=widget.js.map

/***/ }),

/***/ "../dfnotebook/lib/widgetfactory.js":
/*!******************************************!*\
  !*** ../dfnotebook/lib/widgetfactory.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "DataflowNotebookWidgetFactory": () => (/* binding */ DataflowNotebookWidgetFactory)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * A widget factory for notebook panels.
 */
class DataflowNotebookWidgetFactory extends _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.NotebookWidgetFactory {
}
//# sourceMappingURL=widgetfactory.js.map

/***/ })

}]);
//# sourceMappingURL=dfnotebook_lib_index_js.5867814663b3076aa00e.js.map
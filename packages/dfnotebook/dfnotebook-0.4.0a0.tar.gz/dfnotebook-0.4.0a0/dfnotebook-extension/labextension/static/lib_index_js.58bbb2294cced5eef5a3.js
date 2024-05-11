"use strict";
(self["webpackChunk_dfnotebook_dfnotebook_extension"] = self["webpackChunk_dfnotebook_dfnotebook_extension"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_cell_toolbar__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/cell-toolbar */ "webpack/sharing/consume/default/@jupyterlab/cell-toolbar");
/* harmony import */ var _jupyterlab_cell_toolbar__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_cell_toolbar__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/cells */ "webpack/sharing/consume/default/@jupyterlab/cells");
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/codeeditor */ "webpack/sharing/consume/default/@jupyterlab/codeeditor");
/* harmony import */ var _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/filebrowser */ "webpack/sharing/consume/default/@jupyterlab/filebrowser");
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher");
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @jupyterlab/mainmenu */ "webpack/sharing/consume/default/@jupyterlab/mainmenu");
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_9__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_10___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_10__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_11___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_11__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_12___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_12__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_13___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_13__);
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! @lumino/disposable */ "webpack/sharing/consume/default/@lumino/disposable");
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_14___default = /*#__PURE__*/__webpack_require__.n(_lumino_disposable__WEBPACK_IMPORTED_MODULE_14__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_15___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_15__);
/* harmony import */ var _dfnotebook_dfnotebook__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(/*! @dfnotebook/dfnotebook */ "webpack/sharing/consume/default/@dfnotebook/dfnotebook/@dfnotebook/dfnotebook");
/* harmony import */ var _dfnotebook_dfnotebook__WEBPACK_IMPORTED_MODULE_16___default = /*#__PURE__*/__webpack_require__.n(_dfnotebook_dfnotebook__WEBPACK_IMPORTED_MODULE_16__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_17___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_17__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_18__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_18___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_18__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module dfnotebook-extension
 */



















/**
 * The command IDs used by the notebook plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.createNew = 'notebook:create-new';
    CommandIDs.interrupt = 'notebook:interrupt-kernel';
    CommandIDs.restart = 'notebook:restart-kernel';
    CommandIDs.restartClear = 'notebook:restart-clear-output';
    CommandIDs.restartAndRunToSelected = 'notebook:restart-and-run-to-selected';
    CommandIDs.restartRunAll = 'notebook:restart-run-all';
    CommandIDs.reconnectToKernel = 'notebook:reconnect-to-kernel';
    CommandIDs.changeKernel = 'notebook:change-kernel';
    CommandIDs.createConsole = 'notebook:create-console';
    CommandIDs.createOutputView = 'notebook:create-output-view';
    CommandIDs.clearAllOutputs = 'notebook:clear-all-cell-outputs';
    CommandIDs.closeAndShutdown = 'notebook:close-and-shutdown';
    CommandIDs.trust = 'notebook:trust';
    CommandIDs.exportToFormat = 'notebook:export-to-format';
    CommandIDs.run = 'notebook:run-cell';
    CommandIDs.runAndAdvance = 'notebook:run-cell-and-select-next';
    CommandIDs.runAndInsert = 'notebook:run-cell-and-insert-below';
    CommandIDs.runInConsole = 'notebook:run-in-console';
    CommandIDs.runAll = 'notebook:run-all-cells';
    CommandIDs.runAllAbove = 'notebook:run-all-above';
    CommandIDs.runAllBelow = 'notebook:run-all-below';
    CommandIDs.renderAllMarkdown = 'notebook:render-all-markdown';
    CommandIDs.toCode = 'notebook:change-cell-to-code';
    CommandIDs.toMarkdown = 'notebook:change-cell-to-markdown';
    CommandIDs.toRaw = 'notebook:change-cell-to-raw';
    CommandIDs.cut = 'notebook:cut-cell';
    CommandIDs.copy = 'notebook:copy-cell';
    CommandIDs.pasteAbove = 'notebook:paste-cell-above';
    CommandIDs.pasteBelow = 'notebook:paste-cell-below';
    CommandIDs.duplicateBelow = 'notebook:duplicate-below';
    CommandIDs.pasteAndReplace = 'notebook:paste-and-replace-cell';
    CommandIDs.moveUp = 'notebook:move-cell-up';
    CommandIDs.moveDown = 'notebook:move-cell-down';
    CommandIDs.clearOutputs = 'notebook:clear-cell-output';
    CommandIDs.deleteCell = 'notebook:delete-cell';
    CommandIDs.insertAbove = 'notebook:insert-cell-above';
    CommandIDs.insertBelow = 'notebook:insert-cell-below';
    CommandIDs.selectAbove = 'notebook:move-cursor-up';
    CommandIDs.selectBelow = 'notebook:move-cursor-down';
    CommandIDs.extendAbove = 'notebook:extend-marked-cells-above';
    CommandIDs.extendTop = 'notebook:extend-marked-cells-top';
    CommandIDs.extendBelow = 'notebook:extend-marked-cells-below';
    CommandIDs.extendBottom = 'notebook:extend-marked-cells-bottom';
    CommandIDs.selectAll = 'notebook:select-all';
    CommandIDs.deselectAll = 'notebook:deselect-all';
    CommandIDs.editMode = 'notebook:enter-edit-mode';
    CommandIDs.merge = 'notebook:merge-cells';
    CommandIDs.mergeAbove = 'notebook:merge-cell-above';
    CommandIDs.mergeBelow = 'notebook:merge-cell-below';
    CommandIDs.split = 'notebook:split-cell-at-cursor';
    CommandIDs.commandMode = 'notebook:enter-command-mode';
    CommandIDs.toggleAllLines = 'notebook:toggle-all-cell-line-numbers';
    CommandIDs.undoCellAction = 'notebook:undo-cell-action';
    CommandIDs.redoCellAction = 'notebook:redo-cell-action';
    CommandIDs.markdown1 = 'notebook:change-cell-to-heading-1';
    CommandIDs.markdown2 = 'notebook:change-cell-to-heading-2';
    CommandIDs.markdown3 = 'notebook:change-cell-to-heading-3';
    CommandIDs.markdown4 = 'notebook:change-cell-to-heading-4';
    CommandIDs.markdown5 = 'notebook:change-cell-to-heading-5';
    CommandIDs.markdown6 = 'notebook:change-cell-to-heading-6';
    CommandIDs.hideCode = 'notebook:hide-cell-code';
    CommandIDs.showCode = 'notebook:show-cell-code';
    CommandIDs.hideAllCode = 'notebook:hide-all-cell-code';
    CommandIDs.showAllCode = 'notebook:show-all-cell-code';
    CommandIDs.hideOutput = 'notebook:hide-cell-outputs';
    CommandIDs.showOutput = 'notebook:show-cell-outputs';
    CommandIDs.hideAllOutputs = 'notebook:hide-all-cell-outputs';
    CommandIDs.showAllOutputs = 'notebook:show-all-cell-outputs';
    CommandIDs.toggleRenderSideBySideCurrentNotebook = 'notebook:toggle-render-side-by-side-current';
    CommandIDs.setSideBySideRatio = 'notebook:set-side-by-side-ratio';
    CommandIDs.enableOutputScrolling = 'notebook:enable-output-scrolling';
    CommandIDs.disableOutputScrolling = 'notebook:disable-output-scrolling';
    CommandIDs.selectLastRunCell = 'notebook:select-last-run-cell';
    CommandIDs.replaceSelection = 'notebook:replace-selection';
    CommandIDs.autoClosingBrackets = 'notebook:toggle-autoclosing-brackets';
    CommandIDs.toggleCollapseCmd = 'Collapsible_Headings:Toggle_Collapse';
    CommandIDs.collapseAllCmd = 'Collapsible_Headings:Collapse_All';
    CommandIDs.expandAllCmd = 'Collapsible_Headings:Expand_All';
    CommandIDs.copyToClipboard = 'notebook:copy-to-clipboard';
    CommandIDs.tagCell = 'notebook:tag-cell';
})(CommandIDs || (CommandIDs = {}));
/**
 * The name of the factory that creates notebooks.
 */
const FACTORY = 'Notebook';
/**
 * The name of the factory that creates dataflow notebooks.
 */
const DATAFLOW_FACTORY = 'Dataflow Notebook';
// /**
//  * Setting Id storing the customized toolbar definition.
//  */
// const PANEL_SETTINGS = '@jupyterlab/notebook-extension:panel';
/**
 * The id to use on the style tag for the side by side margins.
 */
const SIDE_BY_SIDE_STYLE_ID = 'jp-NotebookExtension-sideBySideMargins';
/**
 * The notebook widget tracker provider.
 */
const trackerPlugin = {
    id: '@dfnotebook/dfnotebook-extension:tracker',
    provides: _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.INotebookTracker,
    requires: [
        _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.INotebookWidgetFactory,
        _dfnotebook_dfnotebook__WEBPACK_IMPORTED_MODULE_16__.IDataflowNotebookWidgetFactory,
        _dfnotebook_dfnotebook__WEBPACK_IMPORTED_MODULE_16__.IDataflowNotebookModelFactory,
        _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_10__.ITranslator
    ],
    optional: [
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette,
        _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_5__.IFileBrowserFactory,
        _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_6__.ILauncher,
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer,
        _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_7__.IMainMenu,
        _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_9__.ISettingRegistry,
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ISessionContextDialogs
    ],
    activate: activateNotebookHandler,
    autoStart: true
};
/**
 * The dataflow notebook cell factory provider.
 */
const contentFactoryPlugin = {
    id: '@dfnotebook/dfnotebook-extension:factory',
    provides: _dfnotebook_dfnotebook__WEBPACK_IMPORTED_MODULE_16__.IDataflowNotebookContentFactory,
    requires: [_jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_4__.IEditorServices],
    autoStart: true,
    activate: (app, editorServices) => {
        const editorFactory = editorServices.factoryService.newInlineEditor;
        return new _dfnotebook_dfnotebook__WEBPACK_IMPORTED_MODULE_16__.DataflowNotebookPanel.ContentFactory({ editorFactory });
    }
};
/**
 * The dataflow notebook widget factory provider.
 */
const widgetFactoryPlugin = {
    id: '@dfnotebook/dfnotebook-extension:widget-factory',
    provides: _dfnotebook_dfnotebook__WEBPACK_IMPORTED_MODULE_16__.IDataflowNotebookWidgetFactory,
    requires: [
        _dfnotebook_dfnotebook__WEBPACK_IMPORTED_MODULE_16__.IDataflowNotebookContentFactory,
        _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_4__.IEditorServices,
        _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_17__.IRenderMimeRegistry,
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ISessionContextDialogs,
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.IToolbarWidgetRegistry,
        _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_10__.ITranslator
    ],
    optional: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_9__.ISettingRegistry],
    activate: activateDataflowWidgetFactory,
    autoStart: true
};
/**
 * The dataflow notebook model factory provider.
 */
const modelFactoryPlugin = {
    id: '@dfnotebook/dfnotebook-extension:model-factory',
    provides: _dfnotebook_dfnotebook__WEBPACK_IMPORTED_MODULE_16__.IDataflowNotebookModelFactory,
    requires: [
        _dfnotebook_dfnotebook__WEBPACK_IMPORTED_MODULE_16__.IDataflowNotebookWidgetFactory
    ],
    optional: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_9__.ISettingRegistry],
    activate: activateDataflowModelFactory,
    autoStart: true,
};
const cellToolbar = {
    id: '@dfnotebook/dfnotebook-extension:cell-toolbar',
    autoStart: true,
    activate: async (app, settingRegistry, toolbarRegistry, translator) => {
        const cellToolbarId = '@jupyterlab/cell-toolbar-extension:plugin';
        const toolbarItems = settingRegistry && toolbarRegistry
            ? (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.createToolbarFactory)(toolbarRegistry, settingRegistry, _jupyterlab_cell_toolbar__WEBPACK_IMPORTED_MODULE_2__.CellBarExtension.FACTORY_NAME, cellToolbarId, translator !== null && translator !== void 0 ? translator : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_10__.nullTranslator)
            : undefined;
        app.docRegistry.addWidgetExtension(DATAFLOW_FACTORY, new _jupyterlab_cell_toolbar__WEBPACK_IMPORTED_MODULE_2__.CellBarExtension(app.commands, toolbarItems));
    },
    optional: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_9__.ISettingRegistry, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.IToolbarWidgetRegistry, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_10__.ITranslator]
};
const plugins = [
    contentFactoryPlugin,
    widgetFactoryPlugin,
    modelFactoryPlugin,
    trackerPlugin,
    cellToolbar
];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);
function activateDataflowModelFactory(app, widgetFactory, settingRegistry) {
    const registry = app.docRegistry;
    // FIXME need to connect settings changes to this modelFactory?
    const modelFactory = new _dfnotebook_dfnotebook__WEBPACK_IMPORTED_MODULE_16__.DataflowNotebookModelFactory({
        disableDocumentWideUndoRedo: widgetFactory.notebookConfig.disableDocumentWideUndoRedo
    });
    registry.addModelFactory(modelFactory);
    return modelFactory;
}
/**
 * Activate the notebook widget factory.
 */
function activateDataflowWidgetFactory(app, contentFactory, editorServices, rendermime, sessionContextDialogs, toolbarRegistry, translator, settingRegistry) {
    const preferKernelOption = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_18__.PageConfig.getOption('notebookStartsKernel');
    // If the option is not set, assume `true`
    const preferKernelValue = preferKernelOption === '' || preferKernelOption.toLowerCase() === 'true';
    // const { commands } = app;
    // let toolbarFactory:
    //   | ((
    //       widget: NotebookPanel
    //     ) =>
    //       | DocumentRegistry.IToolbarItem[]
    //       | IObservableList<DocumentRegistry.IToolbarItem>)
    //   | undefined;
    // // Register notebook toolbar widgets
    // toolbarRegistry.registerFactory<NotebookPanel>(DATAFLOW_FACTORY, 'save', panel =>
    //   DocToolbarItems.createSaveButton(commands, panel.context.fileChanged)
    // );
    // toolbarRegistry.registerFactory<NotebookPanel>(DATAFLOW_FACTORY, 'cellType', panel => {
    //   return ToolbarItems.createCellTypeItem(panel, translator);
    //   }
    // );
    // toolbarRegistry.registerFactory<NotebookPanel>(DATAFLOW_FACTORY, 'kernelName', panel =>
    //   Toolbar.createKernelNameItem(
    //     panel.sessionContext,
    //     sessionContextDialogs,
    //     translator
    //   )
    // );
    // toolbarRegistry.registerFactory<NotebookPanel>(
    //   DATAFLOW_FACTORY,
    //   'executionProgress',
    //   panel => {
    //     return ExecutionIndicator.createExecutionIndicatorItem(
    //       panel,
    //       translator,
    //       settingRegistry?.load(trackerPlugin.id)
    //     );
    //   }
    // );
    // if (settingRegistry) {
    //   // Create the factory
    //   toolbarFactory = createToolbarFactory(
    //     toolbarRegistry,
    //     settingRegistry,
    //     DATAFLOW_FACTORY,
    //     PANEL_SETTINGS,
    //     translator
    //   );
    // }
    const factory = new _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookWidgetFactory({
        name: DATAFLOW_FACTORY,
        fileTypes: ['notebook'],
        modelName: 'dfnotebook',
        defaultFor: ['notebook'],
        preferKernel: preferKernelValue,
        canStartKernel: true,
        rendermime,
        contentFactory,
        editorConfig: _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.StaticNotebook.defaultEditorConfig,
        notebookConfig: _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.StaticNotebook.defaultNotebookConfig,
        mimeTypeService: editorServices.mimeTypeService,
        sessionDialogs: sessionContextDialogs,
        // toolbarFactory,
        translator: translator
    });
    app.docRegistry.addWidgetFactory(factory);
    return factory;
}
// FIXME if we set the model factory on the docRegistry first
// we can prevent the setting in activateNotebookHandler
// also need a way to modify the app commands for run...
// then may be able to get rid of all this code...
/**
 * Activate the notebook handler extension.
 */
function activateNotebookHandler(app, factory, dfFactory, dfModelFactory, translator, palette, browserFactory, launcher, restorer, mainMenu, settingRegistry, sessionDialogs) {
    const trans = translator.load('jupyterlab');
    const services = app.serviceManager;
    const { commands } = app;
    const tracker = new _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookTracker({ namespace: 'notebook' });
    // Fetch settings if possible.
    const jlabTrackerId = '@jupyterlab/notebook-extension:tracker';
    const fetchSettings = settingRegistry
        ? settingRegistry.load(jlabTrackerId)
        : Promise.reject(new Error(`No setting registry for ${jlabTrackerId}`));
    fetchSettings
        .then(settings => {
        updateConfig(factory, settings);
        updateConfig(dfFactory, settings);
        settings.changed.connect(() => {
            updateConfig(factory, settings);
            updateConfig(dfFactory, settings);
        });
        commands.addCommand(CommandIDs.autoClosingBrackets, {
            execute: args => {
                var _a;
                const codeConfig = settings.get('codeCellConfig')
                    .composite;
                const markdownConfig = settings.get('markdownCellConfig')
                    .composite;
                const rawConfig = settings.get('rawCellConfig')
                    .composite;
                const anyToggled = codeConfig.autoClosingBrackets ||
                    markdownConfig.autoClosingBrackets ||
                    rawConfig.autoClosingBrackets;
                const toggled = !!((_a = args['force']) !== null && _a !== void 0 ? _a : !anyToggled);
                [
                    codeConfig.autoClosingBrackets,
                    markdownConfig.autoClosingBrackets,
                    rawConfig.autoClosingBrackets
                ] = [toggled, toggled, toggled];
                void settings.set('codeCellConfig', codeConfig);
                void settings.set('markdownCellConfig', markdownConfig);
                void settings.set('rawCellConfig', rawConfig);
            },
            label: trans.__('Auto Close Brackets for All Notebook Cell Types'),
            isToggled: () => ['codeCellConfig', 'markdownCellConfig', 'rawCellConfig'].some(x => settings.get(x).composite.autoClosingBrackets)
        });
    })
        .catch((reason) => {
        console.warn(reason.message);
        updateTracker({
            editorConfig: factory.editorConfig,
            notebookConfig: factory.notebookConfig,
            kernelShutdown: factory.shutdownOnClose
        });
    });
    // Handle state restoration.
    if (restorer) {
        void restorer.restore(tracker, {
            command: 'docmanager:open',
            args: panel => ({
                path: panel.context.path,
                factory: (panel.context.model instanceof _dfnotebook_dfnotebook__WEBPACK_IMPORTED_MODULE_16__.DataflowNotebookModel) ? DATAFLOW_FACTORY : FACTORY
            }),
            // use notebook or dfnotebook prefix on name here...
            name: panel => panel.context.path,
            when: services.ready
        });
    }
    const registry = app.docRegistry;
    const modelFactory = new _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookModelFactory({
        disableDocumentWideUndoRedo: factory.notebookConfig.disableDocumentWideUndoRedo
    });
    registry.addModelFactory(modelFactory);
    addCommands(app, tracker, translator, sessionDialogs);
    if (palette) {
        populatePalette(palette, translator);
    }
    let id = 0; // The ID counter for notebook panels.
    const ft = app.docRegistry.getFileType('notebook');
    function connectWidgetCreated(factory) {
        factory.widgetCreated.connect((sender, widget) => {
            var _a, _b;
            // If the notebook panel does not have an ID, assign it one.
            widget.id = widget.id || `notebook-${++id}`;
            // Set up the title icon
            widget.title.icon = ft === null || ft === void 0 ? void 0 : ft.icon;
            widget.title.iconClass = (_a = ft === null || ft === void 0 ? void 0 : ft.iconClass) !== null && _a !== void 0 ? _a : '';
            widget.title.iconLabel = (_b = ft === null || ft === void 0 ? void 0 : ft.iconLabel) !== null && _b !== void 0 ? _b : '';
            // Notify the widget tracker if restore data needs to update.
            widget.context.pathChanged.connect(() => {
                void tracker.save(widget);
            });
            // Add the notebook panel to the tracker.
            void tracker.add(widget);
        });
    }
    connectWidgetCreated(factory);
    connectWidgetCreated(dfFactory);
    /**
     * Update the settings of the current tracker.
     */
    function updateTracker(options) {
        tracker.forEach(widget => {
            widget.setConfig(options);
        });
    }
    /**
     * Update the setting values.
     */
    function updateConfig(factory, settings) {
        const code = Object.assign(Object.assign({}, _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.StaticNotebook.defaultEditorConfig.code), settings.get('codeCellConfig').composite);
        const markdown = Object.assign(Object.assign({}, _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.StaticNotebook.defaultEditorConfig.markdown), settings.get('markdownCellConfig').composite);
        const raw = Object.assign(Object.assign({}, _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.StaticNotebook.defaultEditorConfig.raw), settings.get('rawCellConfig').composite);
        factory.editorConfig = { code, markdown, raw };
        factory.notebookConfig = {
            scrollPastEnd: settings.get('scrollPastEnd').composite,
            defaultCell: settings.get('defaultCell').composite,
            recordTiming: settings.get('recordTiming').composite,
            numberCellsToRenderDirectly: settings.get('numberCellsToRenderDirectly')
                .composite,
            remainingTimeBeforeRescheduling: settings.get('remainingTimeBeforeRescheduling').composite,
            renderCellOnIdle: settings.get('renderCellOnIdle').composite,
            observedTopMargin: settings.get('observedTopMargin').composite,
            observedBottomMargin: settings.get('observedBottomMargin')
                .composite,
            maxNumberOutputs: settings.get('maxNumberOutputs').composite,
            showEditorForReadOnlyMarkdown: settings.get('showEditorForReadOnlyMarkdown').composite,
            disableDocumentWideUndoRedo: settings.get('experimentalDisableDocumentWideUndoRedo').composite,
            renderingLayout: settings.get('renderingLayout').composite,
            sideBySideLeftMarginOverride: settings.get('sideBySideLeftMarginOverride')
                .composite,
            sideBySideRightMarginOverride: settings.get('sideBySideRightMarginOverride').composite
        };
        const sideBySideMarginStyle = `.jp-mod-sideBySide.jp-Notebook .jp-Notebook-cell { 
      margin-left: ${factory.notebookConfig.sideBySideLeftMarginOverride} !important;
      margin-right: ${factory.notebookConfig.sideBySideRightMarginOverride} !important;`;
        const sideBySideMarginTag = document.getElementById(SIDE_BY_SIDE_STYLE_ID);
        if (sideBySideMarginTag) {
            sideBySideMarginTag.innerText = sideBySideMarginStyle;
        }
        else {
            document.head.insertAdjacentHTML('beforeend', `<style id="${SIDE_BY_SIDE_STYLE_ID}">${sideBySideMarginStyle}}</style>`);
        }
        factory.shutdownOnClose = settings.get('kernelShutdown')
            .composite;
        modelFactory.disableDocumentWideUndoRedo = settings.get('experimentalDisableDocumentWideUndoRedo').composite;
        updateTracker({
            editorConfig: factory.editorConfig,
            notebookConfig: factory.notebookConfig,
            kernelShutdown: factory.shutdownOnClose
        });
    }
    // Add main menu notebook menu.
    if (mainMenu) {
        populateMenus(app, mainMenu, tracker, translator, sessionDialogs);
    }
    // Utility function to create a new notebook.
    const createNew = (cwd, kernelName) => {
        return commands
            .execute('docmanager:new-untitled', { path: cwd, type: 'notebook' })
            .then(model => {
            if (model != undefined) {
                return commands.execute('docmanager:open', {
                    path: model.path,
                    factory: kernelName == "dfpython3" ? DATAFLOW_FACTORY : FACTORY,
                    kernel: { name: kernelName }
                });
            }
        });
    };
    // Add a command for creating a new notebook.
    commands.addCommand(CommandIDs.createNew, {
        label: args => {
            var _a, _b, _c;
            const kernelName = args['kernelName'] || '';
            if (args['isLauncher'] && args['kernelName'] && services.kernelspecs) {
                return ((_c = (_b = (_a = services.kernelspecs.specs) === null || _a === void 0 ? void 0 : _a.kernelspecs[kernelName]) === null || _b === void 0 ? void 0 : _b.display_name) !== null && _c !== void 0 ? _c : '');
            }
            if (args['isPalette'] || args['isContextMenu']) {
                return trans.__('New Notebook');
            }
            return trans.__('Notebook');
        },
        caption: trans.__('Create a new notebook'),
        icon: args => (args['isPalette'] ? undefined : _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_11__.notebookIcon),
        execute: args => {
            const cwd = args['cwd'] ||
                (browserFactory ? browserFactory.defaultBrowser.model.path : '');
            const kernelName = args['kernelName'] || '';
            return createNew(cwd, kernelName);
        }
    });
    // Add a launcher item if the launcher is available.
    if (launcher) {
        void services.ready.then(() => {
            let disposables = null;
            const onSpecsChanged = () => {
                if (disposables) {
                    disposables.dispose();
                    disposables = null;
                }
                const specs = services.kernelspecs.specs;
                if (!specs) {
                    return;
                }
                disposables = new _lumino_disposable__WEBPACK_IMPORTED_MODULE_14__.DisposableSet();
                for (const name in specs.kernelspecs) {
                    const rank = name === specs.default ? 0 : Infinity;
                    const spec = specs.kernelspecs[name];
                    let kernelIconUrl = spec.resources['logo-64x64'];
                    disposables.add(launcher.add({
                        command: CommandIDs.createNew,
                        args: { isLauncher: true, kernelName: name },
                        category: trans.__('Notebook'),
                        rank,
                        kernelIconUrl,
                        metadata: {
                            kernel: _lumino_coreutils__WEBPACK_IMPORTED_MODULE_13__.JSONExt.deepCopy(spec.metadata || {})
                        }
                    }));
                }
            };
            onSpecsChanged();
            services.kernelspecs.specsChanged.connect(onSpecsChanged);
        });
    }
    return tracker;
}
// Get the current widget and activate unless the args specify otherwise.
function getCurrent(tracker, shell, args) {
    const widget = tracker.currentWidget;
    const activate = args['activate'] !== false;
    if (activate && widget) {
        shell.activateById(widget.id);
    }
    return widget;
}
/**
 * Add the notebook commands to the application's command registry.
 */
function addCommands(app, tracker, translator, sessionDialogs) {
    const trans = translator.load('jupyterlab');
    const { commands, shell } = app;
    sessionDialogs = sessionDialogs !== null && sessionDialogs !== void 0 ? sessionDialogs : _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.sessionContextDialogs;
    const isEnabled = () => {
        return Private.isEnabled(shell, tracker);
    };
    const isEnabledAndSingleSelected = () => {
        return Private.isEnabledAndSingleSelected(shell, tracker);
    };
    const refreshCellCollapsed = (notebook) => {
        var _a, _b;
        for (const cell of notebook.widgets) {
            if (cell instanceof _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_3__.MarkdownCell && cell.headingCollapsed) {
                _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.setHeadingCollapse(cell, true, notebook);
            }
            if (cell.model.id === ((_b = (_a = notebook.activeCell) === null || _a === void 0 ? void 0 : _a.model) === null || _b === void 0 ? void 0 : _b.id)) {
                _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.expandParent(cell, notebook);
            }
        }
    };
    const isEnabledAndHeadingSelected = () => {
        return Private.isEnabledAndHeadingSelected(shell, tracker);
    };
    // Set up signal handler to keep the collapse state consistent
    tracker.currentChanged.connect((sender, panel) => {
        var _a, _b;
        if (!((_b = (_a = panel === null || panel === void 0 ? void 0 : panel.content) === null || _a === void 0 ? void 0 : _a.model) === null || _b === void 0 ? void 0 : _b.cells)) {
            return;
        }
        panel.content.model.cells.changed.connect((list, args) => {
            // Might be overkill to refresh this every time, but
            // it helps to keep the collapse state consistent.
            refreshCellCollapsed(panel.content);
        });
        panel.content.activeCellChanged.connect((notebook, cell) => {
            _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.expandParent(cell, notebook);
        });
    });
    commands.addCommand(CommandIDs.runAndAdvance, {
        label: trans.__('Run Selected Cells'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                const { context, content } = current;
                if (content instanceof _dfnotebook_dfnotebook__WEBPACK_IMPORTED_MODULE_16__.DataflowNotebook) {
                    return _dfnotebook_dfnotebook__WEBPACK_IMPORTED_MODULE_16__.DataflowNotebookActions.runAndAdvance(content, context.sessionContext);
                }
                else {
                    return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.runAndAdvance(content, context.sessionContext);
                }
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.run, {
        label: trans.__("Run Selected Cells and Don't Advance"),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                const { context, content } = current;
                if (content instanceof _dfnotebook_dfnotebook__WEBPACK_IMPORTED_MODULE_16__.DataflowNotebook) {
                    return _dfnotebook_dfnotebook__WEBPACK_IMPORTED_MODULE_16__.DataflowNotebookActions.run(content, context.sessionContext);
                }
                else {
                    return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.run(content, context.sessionContext);
                }
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.runAndInsert, {
        label: trans.__('Run Selected Cells and Insert Below'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                const { context, content } = current;
                if (content instanceof _dfnotebook_dfnotebook__WEBPACK_IMPORTED_MODULE_16__.DataflowNotebook) {
                    return _dfnotebook_dfnotebook__WEBPACK_IMPORTED_MODULE_16__.DataflowNotebookActions.runAndInsert(content, context.sessionContext);
                }
                else {
                    return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.runAndInsert(content, context.sessionContext);
                }
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.runAll, {
        label: trans.__('Run All Cells'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                const { context, content } = current;
                if (content instanceof _dfnotebook_dfnotebook__WEBPACK_IMPORTED_MODULE_16__.DataflowNotebook) {
                    return _dfnotebook_dfnotebook__WEBPACK_IMPORTED_MODULE_16__.DataflowNotebookActions.runAll(content, context.sessionContext);
                }
                else {
                    return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.runAll(content, context.sessionContext);
                }
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.runAllAbove, {
        label: trans.__('Run All Above Selected Cell'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                const { context, content } = current;
                if (content instanceof _dfnotebook_dfnotebook__WEBPACK_IMPORTED_MODULE_16__.DataflowNotebook) {
                    return _dfnotebook_dfnotebook__WEBPACK_IMPORTED_MODULE_16__.DataflowNotebookActions.runAllAbove(content, context.sessionContext);
                }
                else {
                    return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.runAllAbove(content, context.sessionContext);
                }
            }
        },
        isEnabled: () => {
            // Can't run above if there are multiple cells selected,
            // or if we are at the top of the notebook.
            return (isEnabledAndSingleSelected() &&
                tracker.currentWidget.content.activeCellIndex !== 0);
        }
    });
    commands.addCommand(CommandIDs.runAllBelow, {
        label: trans.__('Run Selected Cell and All Below'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                const { context, content } = current;
                if (content instanceof _dfnotebook_dfnotebook__WEBPACK_IMPORTED_MODULE_16__.DataflowNotebook) {
                    return _dfnotebook_dfnotebook__WEBPACK_IMPORTED_MODULE_16__.DataflowNotebookActions.runAllBelow(content, context.sessionContext);
                }
                else {
                    return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.runAllAbove(content, context.sessionContext);
                }
            }
        },
        isEnabled: () => {
            // Can't run below if there are multiple cells selected,
            // or if we are at the bottom of the notebook.
            return (isEnabledAndSingleSelected() &&
                tracker.currentWidget.content.activeCellIndex !==
                    tracker.currentWidget.content.widgets.length - 1);
        }
    });
    commands.addCommand(CommandIDs.renderAllMarkdown, {
        label: trans.__('Render All Markdown Cells'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                const { context, content } = current;
                if (content instanceof _dfnotebook_dfnotebook__WEBPACK_IMPORTED_MODULE_16__.DataflowNotebook) {
                    return _dfnotebook_dfnotebook__WEBPACK_IMPORTED_MODULE_16__.DataflowNotebookActions.renderAllMarkdown(content, context.sessionContext);
                }
                else {
                    return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.renderAllMarkdown(content, context.sessionContext);
                }
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.restart, {
        label: trans.__('Restart Kernel…'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return sessionDialogs.restart(current.sessionContext, translator);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.closeAndShutdown, {
        label: trans.__('Close and Shut Down'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (!current) {
                return;
            }
            const fileName = current.title.label;
            return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                title: trans.__('Shut down the notebook?'),
                body: trans.__('Are you sure you want to close "%1"?', fileName),
                buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton(), _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.warnButton()]
            }).then(result => {
                if (result.button.accept) {
                    return current.context.sessionContext.shutdown().then(() => {
                        current.dispose();
                    });
                }
            });
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.trust, {
        label: () => trans.__('Trust Notebook'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                const { context, content } = current;
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.trust(content).then(() => context.save());
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.restartClear, {
        label: trans.__('Restart Kernel and Clear All Outputs…'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                const { content, sessionContext } = current;
                return sessionDialogs.restart(sessionContext, translator).then(() => {
                    _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.clearAllOutputs(content);
                });
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.restartAndRunToSelected, {
        label: trans.__('Restart Kernel and Run up to Selected Cell…'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                const { context, content } = current;
                if (content instanceof _dfnotebook_dfnotebook__WEBPACK_IMPORTED_MODULE_16__.DataflowNotebook) {
                    return sessionDialogs
                        .restart(current.sessionContext, translator)
                        .then(restarted => {
                        if (restarted) {
                            void _dfnotebook_dfnotebook__WEBPACK_IMPORTED_MODULE_16__.DataflowNotebookActions.runAllAbove(content, context.sessionContext).then(executed => {
                                if (executed || content.activeCellIndex === 0) {
                                    void _dfnotebook_dfnotebook__WEBPACK_IMPORTED_MODULE_16__.DataflowNotebookActions.run(content, context.sessionContext);
                                }
                            });
                        }
                    });
                }
                else {
                    return sessionDialogs
                        .restart(current.sessionContext, translator)
                        .then(restarted => {
                        if (restarted) {
                            void _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.runAllAbove(content, context.sessionContext).then(executed => {
                                if (executed || content.activeCellIndex === 0) {
                                    void _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.run(content, context.sessionContext);
                                }
                            });
                        }
                    });
                }
            }
        },
        isEnabled: isEnabledAndSingleSelected
    });
    commands.addCommand(CommandIDs.restartRunAll, {
        label: trans.__('Restart Kernel and Run All Cells…'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                const { context, content, sessionContext } = current;
                if (content instanceof _dfnotebook_dfnotebook__WEBPACK_IMPORTED_MODULE_16__.DataflowNotebook) {
                    return sessionDialogs
                        .restart(sessionContext, translator)
                        .then(restarted => {
                        if (restarted) {
                            void _dfnotebook_dfnotebook__WEBPACK_IMPORTED_MODULE_16__.DataflowNotebookActions.runAll(content, context.sessionContext);
                        }
                        return restarted;
                    });
                }
                else {
                    return sessionDialogs
                        .restart(sessionContext, translator)
                        .then(restarted => {
                        if (restarted) {
                            void _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.runAll(content, context.sessionContext);
                        }
                        return restarted;
                    });
                }
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.clearAllOutputs, {
        label: trans.__('Clear All Outputs'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.clearAllOutputs(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.clearOutputs, {
        label: trans.__('Clear Outputs'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.clearOutputs(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.interrupt, {
        label: trans.__('Interrupt Kernel'),
        execute: args => {
            var _a;
            const current = getCurrent(tracker, shell, args);
            if (!current) {
                return;
            }
            const kernel = (_a = current.context.sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel;
            if (kernel) {
                return kernel.interrupt();
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.toCode, {
        label: trans.__('Change to Code Cell Type'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.changeCellType(current.content, 'code');
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.toMarkdown, {
        label: trans.__('Change to Markdown Cell Type'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.changeCellType(current.content, 'markdown');
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.toRaw, {
        label: trans.__('Change to Raw Cell Type'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.changeCellType(current.content, 'raw');
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.cut, {
        label: trans.__('Cut Cells'),
        caption: trans.__('Cut the selected cells'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.cut(current.content);
            }
        },
        icon: args => (args.toolbar ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_11__.cutIcon : undefined),
        isEnabled
    });
    commands.addCommand(CommandIDs.copy, {
        label: trans.__('Copy Cells'),
        caption: trans.__('Copy the selected cells'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.copy(current.content);
            }
        },
        icon: args => (args.toolbar ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_11__.copyIcon : ''),
        isEnabled
    });
    commands.addCommand(CommandIDs.pasteBelow, {
        label: trans.__('Paste Cells Below'),
        caption: trans.__('Paste cells from the clipboard'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.paste(current.content, 'below');
            }
        },
        icon: args => (args.toolbar ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_11__.pasteIcon : undefined),
        isEnabled
    });
    commands.addCommand(CommandIDs.pasteAbove, {
        label: trans.__('Paste Cells Above'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.paste(current.content, 'above');
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.duplicateBelow, {
        label: trans.__('Duplicate Cells Below'),
        caption: trans.__('Copy the selected cells and paste them below the selection'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.duplicate(current.content, 'belowSelected');
            }
        },
        icon: args => (args.toolbar ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_11__.duplicateIcon : ''),
        isEnabled
    });
    commands.addCommand(CommandIDs.pasteAndReplace, {
        label: trans.__('Paste Cells and Replace'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.paste(current.content, 'replace');
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.deleteCell, {
        label: trans.__('Delete Cells'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.deleteCells(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.split, {
        label: trans.__('Split Cell'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.splitCell(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.merge, {
        label: trans.__('Merge Selected Cells'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.mergeCells(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.mergeAbove, {
        label: trans.__('Merge Cell Above'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.mergeCells(current.content, true);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.mergeBelow, {
        label: trans.__('Merge Cell Below'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.mergeCells(current.content, false);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.insertAbove, {
        label: trans.__('Insert Cell Above'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.insertAbove(current.content);
            }
        },
        icon: args => (args.toolbar ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_11__.addAboveIcon : undefined),
        isEnabled
    });
    commands.addCommand(CommandIDs.insertBelow, {
        label: trans.__('Insert Cell Below'),
        caption: trans.__('Insert a cell below'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.insertBelow(current.content);
            }
        },
        icon: args => (args.toolbar ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_11__.addBelowIcon : undefined),
        isEnabled
    });
    commands.addCommand(CommandIDs.selectAbove, {
        label: trans.__('Select Cell Above'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.selectAbove(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.selectBelow, {
        label: trans.__('Select Cell Below'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.selectBelow(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.extendAbove, {
        label: trans.__('Extend Selection Above'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.extendSelectionAbove(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.extendTop, {
        label: trans.__('Extend Selection to Top'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.extendSelectionAbove(current.content, true);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.extendBelow, {
        label: trans.__('Extend Selection Below'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.extendSelectionBelow(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.extendBottom, {
        label: trans.__('Extend Selection to Bottom'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.extendSelectionBelow(current.content, true);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.selectAll, {
        label: trans.__('Select All Cells'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.selectAll(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.deselectAll, {
        label: trans.__('Deselect All Cells'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.deselectAll(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.moveUp, {
        label: trans.__('Move Cells Up'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.moveUp(current.content);
            }
        },
        isEnabled,
        icon: args => (args.toolbar ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_11__.moveUpIcon : undefined)
    });
    commands.addCommand(CommandIDs.moveDown, {
        label: trans.__('Move Cells Down'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.moveDown(current.content);
            }
        },
        isEnabled,
        icon: args => (args.toolbar ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_11__.moveDownIcon : undefined)
    });
    commands.addCommand(CommandIDs.toggleAllLines, {
        label: trans.__('Toggle All Line Numbers'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.toggleAllLineNumbers(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.commandMode, {
        label: trans.__('Enter Command Mode'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                current.content.mode = 'command';
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.editMode, {
        label: trans.__('Enter Edit Mode'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                current.content.mode = 'edit';
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.undoCellAction, {
        label: trans.__('Undo Cell Operation'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.undo(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.redoCellAction, {
        label: trans.__('Redo Cell Operation'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.redo(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.changeKernel, {
        label: trans.__('Change Kernel…'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return sessionDialogs.selectKernel(current.context.sessionContext, translator);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.reconnectToKernel, {
        label: trans.__('Reconnect To Kernel'),
        execute: args => {
            var _a;
            const current = getCurrent(tracker, shell, args);
            if (!current) {
                return;
            }
            const kernel = (_a = current.context.sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel;
            if (kernel) {
                return kernel.reconnect();
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.markdown1, {
        label: trans.__('Change to Heading 1'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.setMarkdownHeader(current.content, 1);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.markdown2, {
        label: trans.__('Change to Heading 2'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.setMarkdownHeader(current.content, 2);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.markdown3, {
        label: trans.__('Change to Heading 3'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.setMarkdownHeader(current.content, 3);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.markdown4, {
        label: trans.__('Change to Heading 4'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.setMarkdownHeader(current.content, 4);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.markdown5, {
        label: trans.__('Change to Heading 5'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.setMarkdownHeader(current.content, 5);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.markdown6, {
        label: trans.__('Change to Heading 6'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.setMarkdownHeader(current.content, 6);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.hideCode, {
        label: trans.__('Collapse Selected Code'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.hideCode(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.showCode, {
        label: trans.__('Expand Selected Code'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.showCode(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.hideAllCode, {
        label: trans.__('Collapse All Code'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.hideAllCode(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.showAllCode, {
        label: trans.__('Expand All Code'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.showAllCode(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.hideOutput, {
        label: trans.__('Collapse Selected Outputs'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.hideOutput(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.showOutput, {
        label: trans.__('Expand Selected Outputs'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.showOutput(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.hideAllOutputs, {
        label: trans.__('Collapse All Outputs'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.hideAllOutputs(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.toggleRenderSideBySideCurrentNotebook, {
        label: trans.__('Render Side-by-Side'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                if (current.content.renderingLayout === 'side-by-side') {
                    return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.renderDefault(current.content);
                }
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.renderSideBySide(current.content);
            }
        },
        isEnabled,
        isToggled: args => {
            const current = getCurrent(tracker, shell, Object.assign(Object.assign({}, args), { activate: false }));
            if (current) {
                return current.content.renderingLayout === 'side-by-side';
            }
            else {
                return false;
            }
        }
    });
    commands.addCommand(CommandIDs.setSideBySideRatio, {
        label: trans.__('Set side-by-side ratio'),
        execute: args => {
            _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.InputDialog.getNumber({
                title: trans.__('Width of the output in side-by-side mode'),
                value: 1
            })
                .then(result => {
                if (result.value) {
                    document.documentElement.style.setProperty('--jp-side-by-side-output-size', `${result.value}fr`);
                }
            })
                .catch(console.error);
        }
    });
    commands.addCommand(CommandIDs.showAllOutputs, {
        label: trans.__('Expand All Outputs'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.showAllOutputs(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.enableOutputScrolling, {
        label: trans.__('Enable Scrolling for Outputs'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.enableOutputScrolling(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.disableOutputScrolling, {
        label: trans.__('Disable Scrolling for Outputs'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.disableOutputScrolling(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.selectLastRunCell, {
        label: trans.__('Select current running or last run cell'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.selectLastRunCell(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.replaceSelection, {
        label: trans.__('Replace Selection in Notebook Cell'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            const text = args['text'] || '';
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.replaceSelection(current.content, text);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.toggleCollapseCmd, {
        label: 'Toggle Collapse Notebook Heading',
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.toggleCurrentHeadingCollapse(current.content);
            }
        },
        isEnabled: isEnabledAndHeadingSelected
    });
    commands.addCommand(CommandIDs.collapseAllCmd, {
        label: 'Collapse All Cells',
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.collapseAll(current.content);
            }
        }
    });
    commands.addCommand(CommandIDs.expandAllCmd, {
        label: 'Expand All Headings',
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.expandAllHeadings(current.content);
            }
        }
    });
    commands.addCommand(CommandIDs.tagCell, {
        label: trans.__('Tag Cell'),
        execute: args => {
            var _a;
            const cell = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content.activeCell;
            if (cell == null) {
                return;
            }
            const inputArea = cell.inputArea;
            const value = prompt("Tag this cell please:", "");
            inputArea.addTag(value);
        }
    });
}
/**
 * Populate the application's command palette with notebook commands.
 */
function populatePalette(palette, translator) {
    const trans = translator.load('jupyterlab');
    let category = trans.__('Notebook Operations');
    [
        CommandIDs.interrupt,
        CommandIDs.restart,
        CommandIDs.restartClear,
        CommandIDs.restartRunAll,
        CommandIDs.runAll,
        CommandIDs.renderAllMarkdown,
        CommandIDs.runAllAbove,
        CommandIDs.runAllBelow,
        CommandIDs.restartAndRunToSelected,
        CommandIDs.selectAll,
        CommandIDs.deselectAll,
        CommandIDs.clearAllOutputs,
        CommandIDs.toggleAllLines,
        CommandIDs.editMode,
        CommandIDs.commandMode,
        CommandIDs.changeKernel,
        CommandIDs.reconnectToKernel,
        CommandIDs.createConsole,
        CommandIDs.closeAndShutdown,
        CommandIDs.trust,
        CommandIDs.toggleCollapseCmd,
        CommandIDs.collapseAllCmd,
        CommandIDs.expandAllCmd
    ].forEach(command => {
        palette.addItem({ command, category });
    });
    palette.addItem({
        command: CommandIDs.createNew,
        category,
        args: { isPalette: true }
    });
    category = trans.__('Notebook Cell Operations');
    [
        CommandIDs.run,
        CommandIDs.runAndAdvance,
        CommandIDs.runAndInsert,
        CommandIDs.runInConsole,
        CommandIDs.clearOutputs,
        CommandIDs.toCode,
        CommandIDs.toMarkdown,
        CommandIDs.toRaw,
        CommandIDs.cut,
        CommandIDs.copy,
        CommandIDs.pasteBelow,
        CommandIDs.pasteAbove,
        CommandIDs.pasteAndReplace,
        CommandIDs.deleteCell,
        CommandIDs.split,
        CommandIDs.merge,
        CommandIDs.mergeAbove,
        CommandIDs.mergeBelow,
        CommandIDs.insertAbove,
        CommandIDs.insertBelow,
        CommandIDs.selectAbove,
        CommandIDs.selectBelow,
        CommandIDs.extendAbove,
        CommandIDs.extendTop,
        CommandIDs.extendBelow,
        CommandIDs.extendBottom,
        CommandIDs.moveDown,
        CommandIDs.moveUp,
        CommandIDs.tagCell,
        CommandIDs.undoCellAction,
        CommandIDs.redoCellAction,
        CommandIDs.markdown1,
        CommandIDs.markdown2,
        CommandIDs.markdown3,
        CommandIDs.markdown4,
        CommandIDs.markdown5,
        CommandIDs.markdown6,
        CommandIDs.hideCode,
        CommandIDs.showCode,
        CommandIDs.hideAllCode,
        CommandIDs.showAllCode,
        CommandIDs.hideOutput,
        CommandIDs.showOutput,
        CommandIDs.hideAllOutputs,
        CommandIDs.showAllOutputs,
        CommandIDs.toggleRenderSideBySideCurrentNotebook,
        CommandIDs.setSideBySideRatio,
        CommandIDs.enableOutputScrolling,
        CommandIDs.disableOutputScrolling
    ].forEach(command => {
        palette.addItem({ command, category });
    });
}
/**
 * Populates the application menus for the notebook.
 */
function populateMenus(app, mainMenu, tracker, translator, sessionDialogs) {
    const trans = translator.load('jupyterlab');
    const { commands } = app;
    sessionDialogs = sessionDialogs || _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.sessionContextDialogs;
    // Add undo/redo hooks to the edit menu.
    mainMenu.editMenu.undoers.add({
        tracker: tracker,
        undo: widget => {
            var _a;
            (_a = widget.content.activeCell) === null || _a === void 0 ? void 0 : _a.editor.undo();
        },
        redo: widget => {
            var _a;
            (_a = widget.content.activeCell) === null || _a === void 0 ? void 0 : _a.editor.redo();
        }
    });
    // Add a clearer to the edit menu
    mainMenu.editMenu.clearers.add({
        tracker: tracker,
        clearCurrentLabel: (n) => trans.__('Clear Output'),
        clearAllLabel: (n) => {
            return trans.__('Clear All Outputs');
        },
        clearCurrent: (current) => {
            return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.clearOutputs(current.content);
        },
        clearAll: (current) => {
            return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.clearAllOutputs(current.content);
        }
    });
    // Add a close and shutdown command to the file menu.
    mainMenu.fileMenu.closeAndCleaners.add({
        tracker: tracker,
        closeAndCleanupLabel: (n) => trans.__('Close and Shutdown Notebook'),
        closeAndCleanup: (current) => {
            const fileName = current.title.label;
            return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                title: trans.__('Shut down the Notebook?'),
                body: trans.__('Are you sure you want to close "%1"?', fileName),
                buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton(), _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.warnButton()]
            }).then(result => {
                if (result.button.accept) {
                    return current.context.sessionContext.shutdown().then(() => {
                        current.dispose();
                    });
                }
            });
        }
    });
    // Add a kernel user to the Kernel menu
    mainMenu.kernelMenu.kernelUsers.add({
        tracker: tracker,
        interruptKernel: current => {
            var _a;
            const kernel = (_a = current.sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel;
            if (kernel) {
                return kernel.interrupt();
            }
            return Promise.resolve(void 0);
        },
        reconnectToKernel: current => {
            var _a;
            const kernel = (_a = current.sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel;
            if (kernel) {
                return kernel.reconnect();
            }
            return Promise.resolve(void 0);
        },
        restartKernelAndClearLabel: (n) => trans.__('Restart Kernel and Clear All Outputs…'),
        restartKernel: current => sessionDialogs.restart(current.sessionContext, translator),
        restartKernelAndClear: current => {
            return sessionDialogs
                .restart(current.sessionContext, translator)
                .then(restarted => {
                if (restarted) {
                    _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.clearAllOutputs(current.content);
                }
                return restarted;
            });
        },
        changeKernel: current => sessionDialogs.selectKernel(current.sessionContext, translator),
        shutdownKernel: current => current.sessionContext.shutdown()
    });
    // Add a console creator the the Kernel menu
    mainMenu.fileMenu.consoleCreators.add({
        tracker: tracker,
        createConsoleLabel: (n) => trans.__('New Console for Notebook'),
        createConsole: current => Private.createConsole(commands, current, true)
    });
    // Add an IEditorViewer to the application view menu
    mainMenu.viewMenu.editorViewers.add({
        tracker: tracker,
        toggleLineNumbers: widget => {
            _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.toggleAllLineNumbers(widget.content);
        },
        lineNumbersToggled: widget => {
            const config = widget.content.editorConfig;
            return !!(config.code.lineNumbers &&
                config.markdown.lineNumbers &&
                config.raw.lineNumbers);
        }
    });
    // Add an ICodeRunner to the application run menu
    mainMenu.runMenu.codeRunners.add({
        tracker: tracker,
        runLabel: (n) => trans.__('Run Selected Cells'),
        runCaption: (n) => trans.__('Run the selected cells and advance'),
        runAllLabel: (n) => trans.__('Run All Cells'),
        runAllCaption: (n) => trans.__('Run the all notebook cells'),
        restartAndRunAllLabel: (n) => trans.__('Restart Kernel and Run All Cells…'),
        restartAndRunAllCaption: (n) => trans.__('Restart the kernel, then re-run the whole notebook'),
        run: current => {
            const { context, content } = current;
            if (content instanceof _dfnotebook_dfnotebook__WEBPACK_IMPORTED_MODULE_16__.DataflowNotebook) {
                return _dfnotebook_dfnotebook__WEBPACK_IMPORTED_MODULE_16__.DataflowNotebookActions.runAndAdvance(content, context.sessionContext).then(() => void 0);
            }
            else {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.runAndAdvance(content, context.sessionContext).then(() => void 0);
            }
        },
        runAll: current => {
            const { context, content } = current;
            if (content instanceof _dfnotebook_dfnotebook__WEBPACK_IMPORTED_MODULE_16__.DataflowNotebook) {
                return _dfnotebook_dfnotebook__WEBPACK_IMPORTED_MODULE_16__.DataflowNotebookActions.runAll(content, context.sessionContext).then(() => void 0);
            }
            else {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.runAll(content, context.sessionContext).then(() => void 0);
            }
        },
        restartAndRunAll: current => {
            const { context, content } = current;
            return sessionDialogs
                .restart(context.sessionContext, translator)
                .then(restarted => {
                if (restarted) {
                    if (content instanceof _dfnotebook_dfnotebook__WEBPACK_IMPORTED_MODULE_16__.DataflowNotebook) {
                        void _dfnotebook_dfnotebook__WEBPACK_IMPORTED_MODULE_16__.DataflowNotebookActions.runAll(content, context.sessionContext);
                    }
                    else {
                        void _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_8__.NotebookActions.runAll(content, context.sessionContext);
                    }
                }
                return restarted;
            });
        }
    });
    // Add kernel information to the application help menu.
    mainMenu.helpMenu.kernelUsers.add({
        tracker: tracker,
        getKernel: current => { var _a; return (_a = current.sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel; }
    });
}
/**
 * A namespace for module private functionality.
 */
var Private;
(function (Private) {
    /**
     * Create a console connected with a notebook kernel
     *
     * @param commands Commands registry
     * @param widget Notebook panel
     * @param activate Should the console be activated
     */
    function createConsole(commands, widget, activate) {
        const options = {
            path: widget.context.path,
            preferredLanguage: widget.context.model.defaultKernelLanguage,
            activate: activate,
            ref: widget.id,
            insertMode: 'split-bottom'
        };
        return commands.execute('console:create', options);
    }
    Private.createConsole = createConsole;
    /**
     * Whether there is an active notebook.
     */
    function isEnabled(shell, tracker) {
        return (tracker.currentWidget !== null &&
            tracker.currentWidget === shell.currentWidget);
    }
    Private.isEnabled = isEnabled;
    /**
     * Whether there is an notebook active, with a single selected cell.
     */
    function isEnabledAndSingleSelected(shell, tracker) {
        if (!Private.isEnabled(shell, tracker)) {
            return false;
        }
        const { content } = tracker.currentWidget;
        const index = content.activeCellIndex;
        // If there are selections that are not the active cell,
        // this command is confusing, so disable it.
        for (let i = 0; i < content.widgets.length; ++i) {
            if (content.isSelected(content.widgets[i]) && i !== index) {
                return false;
            }
        }
        return true;
    }
    Private.isEnabledAndSingleSelected = isEnabledAndSingleSelected;
    /**
     * Whether there is an notebook active, with a single selected cell.
     */
    function isEnabledAndHeadingSelected(shell, tracker) {
        if (!Private.isEnabled(shell, tracker)) {
            return false;
        }
        const { content } = tracker.currentWidget;
        const index = content.activeCellIndex;
        if (!(content.activeCell instanceof _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_3__.MarkdownCell)) {
            return false;
        }
        // If there are selections that are not the active cell,
        // this command is confusing, so disable it.
        for (let i = 0; i < content.widgets.length; ++i) {
            if (content.isSelected(content.widgets[i]) && i !== index) {
                return false;
            }
        }
        return true;
    }
    Private.isEnabledAndHeadingSelected = isEnabledAndHeadingSelected;
    /**
     * The default Export To ... formats and their human readable labels.
     */
    function getFormatLabels(translator) {
        translator = translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_10__.nullTranslator;
        const trans = translator.load('jupyterlab');
        return {
            html: trans.__('HTML'),
            latex: trans.__('LaTeX'),
            markdown: trans.__('Markdown'),
            pdf: trans.__('PDF'),
            rst: trans.__('ReStructured Text'),
            script: trans.__('Executable Script'),
            slides: trans.__('Reveal.js Slides')
        };
    }
    Private.getFormatLabels = getFormatLabels;
    /**
     * A widget hosting a cloned output area.
     */
    class ClonedOutputArea extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_15__.Panel {
        constructor(options) {
            super();
            this._cell = null;
            const trans = (options.translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_10__.nullTranslator).load('jupyterlab');
            this._notebook = options.notebook;
            this._index = options.index !== undefined ? options.index : -1;
            this._cell = options.cell || null;
            this.id = `LinkedOutputView-${_lumino_coreutils__WEBPACK_IMPORTED_MODULE_13__.UUID.uuid4()}`;
            this.title.label = 'Output View';
            this.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_11__.notebookIcon;
            this.title.caption = this._notebook.title.label
                ? trans.__('For Notebook: %1', this._notebook.title.label)
                : trans.__('For Notebook:');
            this.addClass('jp-LinkedOutputView');
            // Wait for the notebook to be loaded before
            // cloning the output area.
            void this._notebook.context.ready.then(() => {
                if (!this._cell) {
                    this._cell = this._notebook.content.widgets[this._index];
                }
                if (!this._cell || this._cell.model.type !== 'code') {
                    this.dispose();
                    return;
                }
                const clone = this._cell.cloneOutputArea();
                this.addWidget(clone);
            });
        }
        /**
         * The index of the cell in the notebook.
         */
        get index() {
            return this._cell
                ? _lumino_algorithm__WEBPACK_IMPORTED_MODULE_12__.ArrayExt.findFirstIndex(this._notebook.content.widgets, c => c === this._cell)
                : this._index;
        }
        /**
         * The path of the notebook for the cloned output area.
         */
        get path() {
            return this._notebook.context.path;
        }
    }
    Private.ClonedOutputArea = ClonedOutputArea;
})(Private || (Private = {}));
//# sourceMappingURL=index.js.map

/***/ })

}]);
//# sourceMappingURL=lib_index_js.58bbb2294cced5eef5a3.js.map
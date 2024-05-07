import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin,
  ILabShell,
} from '@jupyterlab/application';
import { ICommandPalette, IWindowResolver } from '@jupyterlab/apputils';
import '../style/index.css'; // 引入自定义CSS文件
import {IFileBrowserFactory, IDefaultFileBrowser} from '@jupyterlab/filebrowser';
import {INotebookTracker } from '@jupyterlab/notebook';
import { checkLogin } from './api';
const { MainAreaWidget } = require('@jupyterlab/apputils');
const { Widget } = require('@lumino/widgets');
import {
  IDocumentManager,
} from '@jupyterlab/docmanager';

/**
 * The command IDs used by the application plugin.
 */
// namespace CommandIDs {
//   export const createConsole = 'notebook:create-console';
// }

/**
 * Initialization data for the didi-notebook-extension extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'didi-notebook-extension:plugin',
  description: 'A JupyterLab extension.',
  autoStart: true,
  requires: [IFileBrowserFactory, IDefaultFileBrowser, IWindowResolver, IDocumentManager, ICommandPalette, INotebookTracker],
  optional: [ILabShell],
  activate: async (
    app: JupyterFrontEnd,
    factory: IFileBrowserFactory,
    fileBrowser: IDefaultFileBrowser,
    resolver: IWindowResolver,
    docManager: IDocumentManager,
    palette: ICommandPalette, 
    tracker: INotebookTracker,
    labShell: ILabShell,
    ) => {
    // const trans = translator.load('jupyterlab');
    const urlParams = new URLSearchParams(window.location.search);
    const urlQueryFrom = urlParams.get('from');
    const urlSaveId =  urlParams.get('saveId');
    const hideMenu: string | false = urlParams.get('hideMenu') || false;
    console.log('-----didi-notebook-extension url query----', urlParams);
    // 创建一个新的Widget
    const content = new Widget();
    content.id = 'didi-notebook-extension-plugin-window';
    content.title.label = 'didi-notebook-extension Window';
    content.title.closable = true;
    // 内嵌在studio中
    if (urlQueryFrom === 'studio') {
      console.log('-----didi-notebook-extension----check from studio------');
      document.body.classList.add('from-studio');
      const isLogin = await checkLogin();
      if (!isLogin) {
        console.log('-----didi-notebook-extension----check login failed------');
        return ;
      }    
      console.log('-----didi-notebook-extension----check login success------')
    
      console.log('------from studio  window------', window);

      content.node.addEventListener('message', (res: any) => {
        console.log('---------didi-notebook-extension content node 收到数据啦啦啦啦啦啦---------', res.data);
        const data = res.data || {};
        if (data.event === 'studio-debug-mode-save') {
          app.commands.execute('docmanager:save');
        }
      }, false);
      window.addEventListener('message', async (res: any) => {
        console.log('--------didi-notebook-extension window 收到数据啦啦啦啦啦啦---------', res.data);
        const data = res.data || {};
        if (data.event === 'studio-debug-mode-save') {

          console.log('--------didi-notebook-extension window docmanager:save 保存文件啦---------');
          app.commands.execute('docmanager:save');
          try {
            const widget = labShell?.currentWidget;
            console.log('--------didi-notebook-extension windowcontextForWidget 保存文件啦---------');
            const context = docManager.contextForWidget(widget!);
            await context?.save();
            console.log('--------didi-notebook-extension windowcontextForWidget context', context);
          } catch(err) {
            console.log('--------didi-notebook-extension window 手动保存文件失败啦-----', err);
          }
          console.log('--------didi-notebook-extension windowcontextForWidget 保存成功啦---------');
          window.parent.postMessage({
            event: 'notebook-extension-file-save',
            id: data?.id || urlSaveId,
            status: true
          }, '*');
        
        } else if (data.event === 'studio-quit-debug-mode') {
          console.log('--------didi-notebook-extension window 手动停止kernel啦---------');
          try {
            app.serviceManager?.sessions?.dispose();
            console.log('--------------didi-notebook-extension Kernel terminated successfully.------------');
          } catch (error: any){
            console.error('--------------didi-notebook-extensionFailed to terminate kernel:', error);
          }
           

         
        }
      }, false);
      const widget = new MainAreaWidget({ content });
      labShell && labShell?.add(widget, 'main');
      // 监听文件保存事件
      factory.createFileBrowser('cur-file').model.fileChanged.connect((sender, args) => {
        if (args.type === 'save') {
          console.log('---didi-notebook-extension-----File saved-------', sender, args);
          window.parent.postMessage({
            event: 'notebook-extension-file-save',
            id: urlSaveId,
            status: true
          }, '*');
        }
      });
    }
    // 隐藏菜单
    if ( hideMenu === 'true' || hideMenu !== false) {

      // 隐藏菜单
      document.body.classList.add('hide-menu');
      if (labShell) { 
        // const contextNode: HTMLElement | undefined = app.contextMenuHitTest(
        //   node => !!node.dataset.id
        // );
        if (labShell.leftCollapsed) {
          labShell.expandLeft();
        }
        if (labShell.rightCollapsed) {
          labShell.expandRight();
        }
        labShell.activeChanged.connect((sender, args) => {
          if (sender.leftCollapsed) {
            sender.expandLeft();
          }
          if (sender.rightCollapsed) {
            sender.expandRight();
          }
        });
      }
    }
    console.log('JupyterLab extension didinotebooktest is activated! log', urlQueryFrom, hideMenu);
    console.log('JupyterLab extension didi-notebook-extension is activated!', window, app, document.getElementsByClassName('moon'));
    // 当前插件加载时 notebook页面渲染的静态资源已经全部加载完成 这个通知是为了去除白屏状态
    window.parent.postMessage({
      event: 'notebook-extension-status',
      status: 'loaded',
      id: urlSaveId,
    }, '*');
  }
};

export default plugin;

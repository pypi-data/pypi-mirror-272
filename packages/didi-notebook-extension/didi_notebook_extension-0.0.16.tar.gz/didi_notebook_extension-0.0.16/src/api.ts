let env = 'online';
if (
    location.hostname.indexOf('notebook-test.bigdata.xiaojukeji.com') !== -1
) {
    env = 'test';
} else if (location.hostname.indexOf('didiglobal.com') !== -1) {
    env = 'global';
}
const ssoAppId = env !== 'global' ? '2101066' : '2824';
// 在你的扩展中
export const checkLogin = async () => {
    console.log('----------didi-notebook-extensio checkLogin-----------');
try {
    const response = await fetch(
        '/api/isLogin',
        // 'http://notebook-test.bigdata.xiaojukeji.com/api/isLogin',
        { method: 'GET' });
    let data: any = response.body;
    console.log('----------didi-notebook-extensio checkLogin success data-----------', data);
    if (data?.code === 10001) {
        let host = 'mis.diditaxi.com.cn';
        if (env === 'global') {
          host = 'mis-auth.didiglobal.com'
        }
        console.log('----------didi-notebook-extensio checkLogin failed data-----------', data);
        // let href = 'http://notebook.bigdata.xiaojukeji.com/';
        // if (env === 'global') {
        //     href = 'http://notebook.bigdata.intra.didiglobal.com/';
        // } else if (env === 'test') {
        //     href = 'http://notebook-test.bigdata.xiaojukeji.com/';
        // }
        const jumpto = encodeURIComponent(location.href);
        window.location.href = `//${host}/auth/sso/login?app_id=${ssoAppId}&jumpto=${jumpto}&callback_index=2`;
    } else if (data.code === 0 || data.code === 10000 || data.code === 14001) {
        return data;
    } 
    return true;
} catch (error) {
    console.error('Failed to check login status:', error);
    return true;
}
};
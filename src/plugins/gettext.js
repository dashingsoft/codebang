// import i18n from 'gettext.js'
let i18n = require('gettext.js').default()

const locales = [
    {
        "": {
            "language": "en-US",
            "plural-forms": "nplurals=2; plural=n>1;"
        },
        "代码帮": "CodeBang",
        "代码": "Code",
        "编译": "Build",
        "运行": "Launch",
        "请输入搜索内容": "Please input search text",
        "登陆为 %1": "Signed in as %1",
        "登陆": "Sign in",
        "注销": "Sign out",
        "设置": "Settings",
    }
]

locales.forEach( data => i18n.loadJSON( data ) )

const I18nPlugin = {

    install( Vue ) {
        Vue.prototype.$t = function () {
            return i18n.gettext.apply( i18n, arguments )
        }
    }

}

function gettext () {
    return i18n.gettext.apply( i18n, arguments )
}

function setLocale ( lang ) {

    i18n.setLocale( lang )
    // i18n.setLocaleMessage( lang, require( './locale/messages-' + lang ).default )

}

export { I18nPlugin as default, setLocale, gettext as _t }

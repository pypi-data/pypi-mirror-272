from flask import Flask, render_template_string
from importlib import import_module
from . import core, config
import xhlog as log

app = Flask("ApiCat")

@app.route('/')
def docs():
    plugin_docs = {}
    for blueprint_name in app.blueprints:
        module_name = blueprint_name.replace('-', '_')  # 转换为模块导入格式
        try:
            module = import_module(module_name)
            plugin_docs[blueprint_name] = getattr(module, 'docs', None)
        except (ImportError, AttributeError):
            log.error(f"插件 {blueprint_name} 没有文档。")

    combined_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{config.get_website_name()}</title>
        </head>
        <body>
            <h1>{config.get_website_name()}</h1>
            """

    for plugin_name, docs_func in plugin_docs.items():
        docs_str = docs_func() if callable(docs_func) else str(docs_func)
        combined_html += f"""
            <div class="api-docs">
                <p>{docs_str}</p>
            </div>
            """

    combined_html += """
            <br>
            <footer>
                <p>Powered by <a href="https://github.com/xinghai-osc/apicat">ApiCat</a></p>
            </footer>
        </body>
        <style>
    body {
        font-family: Arial, sans-serif;
        line-height: 1.6;
        color: #333;
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    /* 主标题样式 */
    h1 {
        font-size: 2rem;
        text-align: center;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }

    /* API文档容器 */
    .api-docs {
        background-color: #f9f9f9;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    /* 文本内容 */
    p {
        margin-bottom: 1rem;
    }

    /* 底部信息 */
    footer {
        text-align: center;
        margin-top: 3rem;
        color: #777;
    }
    
    /* "Powered by" 链接样式 */
    footer a {
        color: #007BFF;
        text-decoration: none;
    }
    
    footer a:hover {
        text-decoration: underline;
    }

    /* 响应式设计 */
    @media (max-width: 768px) {
        h1 {
            font-size: 1.5rem;
        }
        
        .plugin-docs {
            padding: 10px;
        }
    }
</style>
        </html>
        """
    return render_template_string(combined_html)

def start(plugin_list: list):
    log.info("欢迎使用 ApiCat🎉")
    log.info("开发团队: 星海码队")
    log.info("项目地址: https://github.com/xinghai-osc/apicat")
    core.register_plugins(plugin_list, app)
    app.run(port=config.get_port(), host=config.get_host())
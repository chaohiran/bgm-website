from flask import Flask, send_from_directory
from config import Config
from services.i18n import t, get_lang, SUPPORTED_LANGS

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = "super-secret-key-change-this"

    from routes.home import home_bp
    from routes.products import products_bp
    from routes.pages import pages_bp
    from routes.lang import lang_bp
    from routes.admin_auth import admin_auth_bp
    from routes.admin_products import admin_products_bp
    from routes.admin_categories import admin_categories_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(products_bp, url_prefix="/products")
    app.register_blueprint(pages_bp, url_prefix="/pages")
    app.register_blueprint(lang_bp, url_prefix="/lang")
    app.register_blueprint(admin_auth_bp)
    app.register_blueprint(admin_products_bp)
    app.register_blueprint(admin_categories_bp)

    # ✅ FIXED CONTEXT PROCESSOR
    @app.context_processor
    def inject_i18n():
        return {
            "t": t,
            "current_lang": get_lang(),
            "supported_langs": SUPPORTED_LANGS
        }

    # sitemap
    @app.route("/sitemap.xml")
    def sitemap():
        return send_from_directory("static", "sitemap.xml")

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
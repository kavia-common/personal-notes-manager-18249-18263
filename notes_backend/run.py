from app import create_app

app = create_app()

if __name__ == "__main__":
    # PUBLIC_INTERFACE
    # Entry point for development server.
    app.run()

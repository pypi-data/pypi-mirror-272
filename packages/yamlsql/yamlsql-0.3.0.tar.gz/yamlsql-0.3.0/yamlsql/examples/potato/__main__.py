import uvicorn

if __name__ == "__main__":  # pragma: no cover
    uvicorn.run(
        # Reference the app
        "yamlsql.examples.potato.app:app",
        # # Set host and port
        # host=self.host,
        # port=self.port,
        # Auto-reload when source code changes
        reload=True,
        # Configure logging inside uvicorn
        # log_config=self.logging_config,
        # log_level=self.log_level,
    )

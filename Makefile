test-publish:
	@rye publish --repository testpypi --repository-url https://test.pypi.org/legacy/ --token $TEST_PYPI_TOKEN

publish:
	@rye publish --repository pypi --token $PYPI_TOKEN --yes
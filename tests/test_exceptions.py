"""Tests for mlbapi.exceptions"""
import pytest
import mlbapi.exceptions


class TestExceptionHierarchy:
    def test_mlbapi_exception_is_exception(self):
        assert issubclass(mlbapi.exceptions.MLBAPIException, Exception)

    def test_request_exception_is_mlbapi_exception(self):
        assert issubclass(mlbapi.exceptions.RequestException,
                          mlbapi.exceptions.MLBAPIException)

    def test_implementation_exception_is_mlbapi_exception(self):
        assert issubclass(mlbapi.exceptions.ImplementationException,
                          mlbapi.exceptions.MLBAPIException)

    def test_object_not_found_exception_is_mlbapi_exception(self):
        assert issubclass(mlbapi.exceptions.ObjectNotFoundException,
                          mlbapi.exceptions.MLBAPIException)

    def test_parameter_exception_is_mlbapi_exception(self):
        assert issubclass(mlbapi.exceptions.ParameterException,
                          mlbapi.exceptions.MLBAPIException)


class TestExceptionRaising:
    def test_raise_mlbapi_exception(self):
        with pytest.raises(mlbapi.exceptions.MLBAPIException):
            raise mlbapi.exceptions.MLBAPIException('base error')

    def test_raise_request_exception(self):
        with pytest.raises(mlbapi.exceptions.RequestException, match='network error'):
            raise mlbapi.exceptions.RequestException('network error')

    def test_raise_implementation_exception(self):
        with pytest.raises(mlbapi.exceptions.ImplementationException, match='not implemented'):
            raise mlbapi.exceptions.ImplementationException('not implemented')

    def test_raise_object_not_found_exception(self):
        with pytest.raises(mlbapi.exceptions.ObjectNotFoundException, match='not found'):
            raise mlbapi.exceptions.ObjectNotFoundException('not found')

    def test_raise_parameter_exception(self):
        with pytest.raises(mlbapi.exceptions.ParameterException, match='invalid param'):
            raise mlbapi.exceptions.ParameterException('invalid param')

    def test_catch_subclass_as_base(self):
        with pytest.raises(mlbapi.exceptions.MLBAPIException):
            raise mlbapi.exceptions.ParameterException('caught as base')

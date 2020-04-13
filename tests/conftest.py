#!/usr/bin/env python

import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--survey_id", action="store", default="SV_bBqGx44QtiQben3", help="Qualtrics SurveyID (begins with 'SV_')"
    )
    parser.addoption(
        "--ml_id", action="store", default="ML_6EeyQ0GukCylanz", help="Qualtrics MailingListID (begins with 'ML_')"
    )

@pytest.fixture
def survey_id(request):
    return request.config.getoption("--survey_id")

@pytest.fixture
def ml_id(request):
    return request.config.getoption("--ml_id")

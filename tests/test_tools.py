#!/usr/bin/env python

import pandas as pd
import pytest
import py_qualtrics_api as pqa
import time


@pytest.fixture
def api_instance():
    return pqa.QualtricsAPI('config_test.yml')

@pytest.fixture
def mail_list_recs():
    em = ['joe.sample@example.com', 'sally.smith@somewhere.net']
    fn = ['Joe', 'Sally']
    ln = ['Sample', 'Smith']
    xref = ['123-45-6789', '987-65-4321']
    retval = pd.DataFrame.from_dict({'email': em, 'firstName': fn,
                                     'lastName': ln, 'externalReference': xref})
    return retval

def test_init(api_instance):
    assert hasattr(api_instance, 'config')
    assert type(api_instance.config.api_token) is str
    assert len(api_instance.config.api_token) == 40
    assert type(api_instance.config.data_center) is str

def test_create_response_export(api_instance, survey_id):
    xpt_id = api_instance.create_response_export(survey_id)
    status = 'incomplete'
    while status != 'complete':
        time.sleep(5)
        status, file_id = api_instance.get_response_export_progress(survey_id, xpt_id)
    df = api_instance.get_response_export_file_as_dataframe(survey_id, file_id)
    assert df.shape[0] == 3

def test_get_response_as_dataframe(api_instance, survey_id, poll_interval=5,
                                   limit=5, use_labels=True,
                                   seen_unanswered_recode=-99,
                                   include_display_order=True,
                                   breakout_sets=True):
    df = api_instance.get_response_as_dataframe(survey_id=survey_id,
                                                poll_interval=poll_interval,
                                                limit=limit,
                                                use_labels=use_labels,
                                    seen_unanswered_recode=seen_unanswered_recode,
                                    include_display_order=include_display_order,
                                    breakout_sets=breakout_sets)
    assert df.shape == (3, 21)

def test_list_users(api_instance):
    df = api_instance.list_users()
    assert df.shape[0] > 0
    assert df.shape[1] == 8

def test_list_surveys(api_instance):
    df = api_instance.list_surveys()
    assert df.shape[0] > 0
    assert df.shape[1] == 6

def test_find_survey_id_exists(api_instance, survey_id, search_str='fake'):
    svyid = api_instance.find_survey_id(search_str=search_str)
    assert svyid == survey_id

def test_find_survey_id_not_exists(api_instance, survey_id, search_str='orange'):
    with pytest.raises(ValueError, match=r"^No surveys matched"):
        api_instance.find_survey_id(search_str=search_str)

def test_find_survey_id_many_exist(api_instance, survey_id, search_str='Reorg'):
    with pytest.raises(ValueError, match=r"multiple surveys"):
        api_instance.find_survey_id(search_str=search_str)

def test_list_mailing_lists(api_instance):
    mlists = api_instance.list_mailing_lists()
    assert mlists.shape[0] > 0

def test_find_mailing_list_id_exists(api_instance, ml_id, search_str='Staff'):
    mlid = api_instance.find_mailing_list_id(search_str=search_str)
    assert mlid == ml_id

def test_find_mailing_list_id_not_exists(api_instance, ml_id,
                                         search_str='orange'):
    with pytest.raises(ValueError, match=r"^No mailing lists matched"):
        api_instance.find_mailing_list_id(search_str=search_str)

def test_find_mailing_list_id_many_exist(api_instance, ml_id,
                                         search_str='Team'):
    with pytest.raises(ValueError, match=r"multiple mailing lists"):
        api_instance.find_mailing_list_id(search_str=search_str)

def test_update_mailing_list(api_instance, ml_id,
                             records_to_add=mail_list_recs):
    with pytest.raises(NotImplementedError, match=r"^The update_mailing_list method is not fully implemented"):
        api_instance.update_mailing_list(ml_id, records_to_add)

def test_create_contacts_bulk(api_instance, ml_id, mail_list_recs):
    rslt = api_instance.create_contacts_bulk(ml_id, mail_list_recs,
                                                  unsubscribed=False,
                                                  language='en', verbose=False)
    assert rslt.startswith('PGRS_')

def test_get_contacts(api_instance, ml_id):
    rslt = api_instance.get_contacts(ml_id, verbose=False)
    assert rslt.shape[1] == 10
    assert rslt.loc[rslt['id'].str.startswith('MLRP_'),].shape[0] == rslt.shape[0]

def test_create_mailing_list(api_instance, mail_list_recs,
                             list_name='My test list', list_category='Test'):
    rslt = api_instance.create_mailing_list(list_name, mail_list_recs,
                                            list_category)
    assert rslt.startswith('ML_')

def test_mailing_list_crud(api_instance, verbose=True):
    mlst = api_instance.list_mailing_lists()
    assert mlst.shape[1] == 5
    if mlst.shape[0]:
        dellst = mlst.loc[mlst['category']=='Test', 'id'].values
    if hasattr(dellst, '__iter__'):
        for lst in dellst:
            resp = api_instance.delete_mailing_list(lst, verbose=verbose)
            assert resp
    elif len(dellst):
        resp = api_instance.delete_mailing_list(dellst, verbose=verbose)
        assert resp
    resp = api_instance.create_mailing_list('My test list',
                                            list_category='Test',
                                            verbose=verbose)
    assert resp.startswith('ML_')
    resp = api_instance.create_mailing_list('My test list', mail_list_recs,
                                            list_category='Test',
                                            verbose=verbose)
    assert resp.startswith('ML_')

# -*- coding: utf-8 -*-
from __future__ import absolute_import
from datetime import datetime
import logging

from utils import (
    setup_redis, setup_queue, Popper
)
from rq.decorators import job

from reports import get_reports, render_reports

logger = logging.getLogger('shera')

def deliver_reports(setupo, contracts_path, reports_path, 
        template, output_path, bucket=500):
    reports = get_reports(contracts_path, reports_path)
    popper = Popper(reports)
    pops = popper.pop(bucket)
    while pops:
        j = push_reports.delay(setupo, pops, template, output_path)
        logger.info("Job id:%s | %s/%s" % (
            j.id, len(pops), len(popper.items))
        )
        pops = popper.pop(bucket)

@job(setup_queue(name='reports'), connection=setup_redis(), timeout=3600)
def push_reports(setupo, reports, template, output):
    O = setupo
    start = datetime.now()
    try:
        render_reports(O, reports, template, output)
        O.send_reports(reports)
    except Exception as e:
        logger.error('Report push failed: %s' % str(e))
    stop = datetime.now()
    logger.info('Delivered reports in %s' % (stop - start))
    logger.info("%s delivered reports" % len(reports))

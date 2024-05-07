from __future__ import print_function

from finter.rest import ApiException

import finter
from finter.settings import get_api_client, logger

from collections import namedtuple
from importlib import import_module


class ContentModelLoader(object):
    __MODULE_CLASS = namedtuple("__MODULE_CLASS", ["module", "loader"])
    __CM_MAP = {
        "content.fnguide.ftp.financial": __MODULE_CLASS(
            "finter.framework_model.content_loader.krx.fnguide.financial", "KrFinancialLoader"),
        "content.fnguide.ftp.consensus": __MODULE_CLASS(
            "finter.framework_model.content_loader.krx.fnguide.consensus", "KrConsensusLoader"),
        "content.fnguide.ftp.economy": __MODULE_CLASS(
            "finter.framework_model.content_loader.krx.fnguide.economy", "EconomyLoader"),
        "content.fnguide.ftp.investor_activity": __MODULE_CLASS(
            "finter.framework_model.content_loader.krx.fnguide.stock", "StockLoader"),
        "content.fnguide.ftp.credit": __MODULE_CLASS(
            "finter.framework_model.content_loader.krx.fnguide.stock", "StockLoader"),
        "content.fnguide.ftp.cax": __MODULE_CLASS(
            "finter.framework_model.content_loader.krx.fnguide.stock", "StockLoader"),
        "content.fnguide.ftp.status": __MODULE_CLASS(
            "finter.framework_model.content_loader.krx.fnguide.stock", "StockLoader"),
        "content.fnguide.ftp.price_volume": __MODULE_CLASS(
            "finter.framework_model.content_loader.krx.fnguide.price_volume", "PriceVolumeLoader"),
        "content.fnguide.ftp.capital": __MODULE_CLASS(
            "finter.framework_model.content_loader.krx.fnguide.capital", "CapitalLoader"),
        "content.quantit.fnguide_cm.factor": __MODULE_CLASS(
            "finter.framework_model.content_loader.di.loader.di", "DILoader"),
        "content.quantit.fnguide_cm.descriptor": __MODULE_CLASS(
            "finter.framework_model.content_loader.krx.fnguide.descriptor", "DescriptorLoader"),
    }

    @classmethod
    def load(cls, key):
        for k, md_class in cls.__CM_MAP.items():
            if key.startswith(k):
                module = import_module(md_class.module)
                attr = getattr(module, md_class.loader)
                if key != k:
                    return attr(key)
                else:
                    return attr

        # Todo: Current __CM_MAP only supports fnguide data.
        return GetCMGetDf(identity_name=key)


class GetCMGetDf(object):
    def __init__(self, identity_name):
        self.identity_name = identity_name

    def get_df(self, start, end, code_format="fnguide_to_quantit", **kwargs):
        # if start or end is str, convert it to str
        param = {
            "identity_name": self.identity_name,
            "start": str(start),
            "end": str(end),
            "code_format": code_format
        }
        param.update(kwargs)
        if ("fnguide" in self.identity_name) and (code_format == "fnguide_to_quantit"):
            param["code_format"] = "fnguide_to_quantit"
        try:
            api_response = finter.AlphaApi(get_api_client()).alpha_base_alpha_cm_retrieve(**param)
            response = api_response.to_dict()
            return finter.to_dataframe(response["cm"], response["column_types"])
        except ApiException as e:
            logger.error("Exception when calling AlphaApi->alpha_base_alpha_cm_retrieve: %s\n" % e)
        return

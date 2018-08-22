# -*- coding: utf-8 -*-
"""

Script Name: config.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python

try:
    from importlib import reload
except ImportError:
    pass

PLATFORM = 'Windows'
API_MINIMUM = 0.64

from core.paths import *

# -------------------------------------------------------------------------------------------------------------
""" DAMG team """

__envKey__          = "PIPELINE_MANAGER"
__organization__    = "DAMGteam"
__groupname__       = "DAMGteam"
__damgSlogan__      = "Comprehensive Solution Design"
__website__         = "https://damgteam.com"
__author1__         = "Trinh Do"
__author2__         = "Duong Minh Duc"
__Founder__         = __author1__
__CoFonder1__       = __author2__
__email1__          = "dot@damgteam.com"
__email2__          = "up@damgteam.com"

# -------------------------------------------------------------------------------------------------------------
""" PipelineTool """

__project__             = "Pipeline Manager (Plm)"
__appname__             = "PLM"
__appShortcut__         = "Plm.ink"
__version__             = "13.0.1"
__cfgVersion__          = "0.8.6"
__verType__             = "Dev"
__reverType__           = "2"
__about__               = "About Pipeline Manager"
__homepage__            = "https://pipeline.damgteam.com"
__plmSlogan__           = "Creative your own pipeline"
__plmWiki__             = "https://github.com/vtta2008/PipelineTool/wiki"

# -------------------------------------------------------------------------------------------------------------
""" Server """

__serverLocal__         = "http://127.0.0.1:8000/"
__serverUrl__           = "https://pipeline.damgteam.com"
__serverCheck__         = "https://pipeline.damgteam.com/check"
__serverAutho__         = "https://pipeline.damgteam.com/auth"
__google__              = "https://google.com.vn"

# -------------------------------------------------------------------------------------------------------------
""" Metadata """

VERSION                 = "{0} v{1}.{2}-{3}".format(__project__, __version__, __verType__, __reverType__)
COPYRIGHT               = "{0} software (c) 2017-2018 {1}. All rights reserved.".format(__appname__, __organization__)
PLUGINVERSION           = "{0}.13.cfg.{1}".format(__appname__, __cfgVersion__)
PLMAPPID                = "{0}.{1}.{2}.{3}".format(__organization__, __project__, __appname__, VERSION)

API_MAJOR_VERSION       = 0.69
API_REVISION            = 0
API_VERSION             = float('%s%s' % (API_MAJOR_VERSION, API_REVISION))
API_VERSION_AS_STRING   = '%.02f.%d' % (API_MAJOR_VERSION, API_REVISION)
PLATFORM                = 'Windows'
API_MINIMUM             = 0.64

# ----------------------------------------------------------------------------------------------------------- #
""" Setup.py options """

__email__               = __email1__ + ", " + __email2__
__packages_dir__        = ["", 'appData', 'bin', 'core', 'imgs', 'plg_ins', 'ui', 'utilities']
__download__            = "https://github.com/vtta2008/PipelineTool/releases"
__description__         = "This applications can be used to build, manage, and optimise film making pipelines."
__readme__              = "README.rst"
__pkgsReq__             = ['appdirs', 'deprecate', 'msgpack', 'winshell', 'pandas', 'wheel', 'argparse', 'green']
__modules__             = []
__classifiers__         = [

    "Development Status :: 3 - Production/Unstable" , "Environment :: X11 Applications :: Qt"                       ,
    "Environment :: Win64 (MS Windows)"             , "Intended Audience :: Freelance Artist :: small VFX studio"   ,
    "License :: OSI Approved :: MIT License"        , "Operating System :: Microsoft :: Windows"                    ,
    "Programming Language :: Python :: 3.6"         ,

    "Topic :: Software Development :: pipeline-framework :: Application :: vfx :: customization :: optimization :: research-project",
                    ]

def reload_module(module):
    return reload(module)

def read_file(fileName):

    filePth = os.path.join(os.getenv(__envKey__), 'appData', 'docs', fileName)
    if not os.path.exists(filePth):
        filePth = os.path.join(os.getenv(__envKey__), 'scr', 'appData', 'docs', fileName)

    with open(filePth, 'r') as f:
        data = f.read()
    return data

QUESTIONS = read_file('QUESTION')
ABOUT = read_file('ABOUT')
CREDIT = read_file('CREDIT')
CODECONDUCT = read_file('CODECONDUCT')
CONTRIBUTING = read_file('CONTRIBUTING')
REFERENCE = read_file('REFERENCE')
LICENCE_MIT = read_file('LICENCE_MIT')

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/06/2018 - 10:56 PM
# Pipeline manager - DAMGteam
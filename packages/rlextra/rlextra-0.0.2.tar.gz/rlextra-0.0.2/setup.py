#Copyright ReportLab Europe Ltd. 2000-2021
#see license.txt for license details
import os, sys

def main():
    from setuptools import setup, find_packages
    if 'sdist' not in sys.argv:
        print("""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!                                                                   ! 
! This is a dummy version of rlextra intended to provide protection !
! against namesquatting in pypi.                                    !
!                                                                   !
! To obtain the ReportLab version of rlextra you need to use        !
!                                                                   !
!   pip install -i"https://www.reportlab.com/pypi" rlextra          !
!                                                                   !
! hope this helps                                                   !
!                                                                   !
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
""")
        sys.exit(1)

    setup(
        name="rlextra",
        version='0.0.2',
        license="BSD license (see license.txt for details), Copyright (c) 2000-2023, ReportLab Inc.",
        description="anti name squatting version of rlextra package",
        long_description="""anti name squatting version of rlextra package""",

        author="Smeaton, Robinson, Becker",
        author_email="info@reportlab.com",
        url="http://www.reportlab.com/",
        packages = find_packages("src"),
        package_dir = {'': "src"},
        install_requires=[
            'reportlab==4.2.0', 
            ],
        extras_require={},
        )

if __name__=='__main__':
    main()

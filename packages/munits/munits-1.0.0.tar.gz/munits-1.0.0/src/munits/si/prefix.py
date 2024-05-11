"""SI-related units of different magnitudes."""

from math import radians
from typing import Final

from .. import DerivedUnit
from . import (
    AMPERE,
    BECQUEREL,
    CANDELA,
    COULOMB,
    FARAD,
    GRAY,
    HENRY,
    HERTZ,
    JOULE,
    KATAL,
    KELVIN,
    KILOGRAM,
    LITRE,
    LUMEN,
    LUX,
    METRE,
    MOLE,
    NEWTON,
    OHM,
    PASCAL,
    RADIAN,
    SECOND,
    SIEMENS,
    SIEVERT,
    STERADIAN,
    TESLA,
    VOLT,
    WATT,
    WEBER,
)

__all__ = [
    "ARC_MINUTE",
    "ARC_SECOND",
    "ATTOAMPERE",
    "ATTOBECQUEREL",
    "ATTOCANDELA",
    "ATTOCOULOMB",
    "ATTOFARAD",
    "ATTOGRAM",
    "ATTOGRAY",
    "ATTOHENRY",
    "ATTOHERTZ",
    "ATTOJOULE",
    "ATTOKATAL",
    "ATTOKELVIN",
    "ATTOLITRE",
    "ATTOLUMEN",
    "ATTOLUX",
    "ATTOMETRE",
    "ATTOMOLE",
    "ATTONEWTON",
    "ATTOOHM",
    "ATTOPASCAL",
    "ATTORADIAN",
    "ATTOSECOND",
    "ATTOSIEMENS",
    "ATTOSIEVERT",
    "ATTOSTERADIAN",
    "ATTOTESLA",
    "ATTOVOLT",
    "ATTOWATT",
    "ATTOWEBER",
    "CENTIAMPERE",
    "CENTIBECQUEREL",
    "CENTICANDELA",
    "CENTICOULOMB",
    "CENTIFARAD",
    "CENTIGRAM",
    "CENTIGRAY",
    "CENTIHENRY",
    "CENTIHERTZ",
    "CENTIJOULE",
    "CENTIKATAL",
    "CENTIKELVIN",
    "CENTILITRE",
    "CENTILUMEN",
    "CENTILUX",
    "CENTIMETRE",
    "CENTIMOLE",
    "CENTINEWTON",
    "CENTIOHM",
    "CENTIPASCAL",
    "CENTIRADIAN",
    "CENTISECOND",
    "CENTISIEMENS",
    "CENTISIEVERT",
    "CENTISTERADIAN",
    "CENTITESLA",
    "CENTIVOLT",
    "CENTIWATT",
    "CENTIWEBER",
    "CENTURY",
    "DAY",
    "DECAAMPERE",
    "DECABECQUEREL",
    "DECACANDELA",
    "DECACOULOMB",
    "DECADE",
    "DECAFARAD",
    "DECAGRAM",
    "DECAGRAY",
    "DECAHENRY",
    "DECAHERTZ",
    "DECAJOULE",
    "DECAKATAL",
    "DECAKELVIN",
    "DECALITRE",
    "DECALUMEN",
    "DECALUX",
    "DECAMETRE",
    "DECAMOLE",
    "DECANEWTON",
    "DECAOHM",
    "DECAPASCAL",
    "DECASECOND",
    "DECASIEMENS",
    "DECASIEVERT",
    "DECATESLA",
    "DECAVOLT",
    "DECAWATT",
    "DECAWEBER",
    "DECIAMPERE",
    "DECIBECQUEREL",
    "DECICANDELA",
    "DECICOULOMB",
    "DECIFARAD",
    "DECIGRAM",
    "DECIGRAY",
    "DECIHENRY",
    "DECIHERTZ",
    "DECIJOULE",
    "DECIKATAL",
    "DECIKELVIN",
    "DECILITRE",
    "DECILUMEN",
    "DECILUX",
    "DECIMETRE",
    "DECIMOLE",
    "DECINEWTON",
    "DECIOHM",
    "DECIPASCAL",
    "DECIRADIAN",
    "DECISECOND",
    "DECISIEMENS",
    "DECISIEVERT",
    "DECISTERADIAN",
    "DECITESLA",
    "DECIVOLT",
    "DECIWATT",
    "DECIWEBER",
    "DEGREE",
    "EXAAMPERE",
    "EXABECQUEREL",
    "EXACANDELA",
    "EXACOULOMB",
    "EXAFARAD",
    "EXAGRAM",
    "EXAGRAY",
    "EXAHENRY",
    "EXAHERTZ",
    "EXAJOULE",
    "EXAKATAL",
    "EXAKELVIN",
    "EXALITRE",
    "EXALUMEN",
    "EXALUX",
    "EXAMETRE",
    "EXAMOLE",
    "EXANEWTON",
    "EXAOHM",
    "EXAPASCAL",
    "EXASECOND",
    "EXASIEMENS",
    "EXASIEVERT",
    "EXATESLA",
    "EXAVOLT",
    "EXAWATT",
    "EXAWEBER",
    "FEMTOAMPERE",
    "FEMTOBECQUEREL",
    "FEMTOCANDELA",
    "FEMTOCOULOMB",
    "FEMTOFARAD",
    "FEMTOGRAM",
    "FEMTOGRAY",
    "FEMTOHENRY",
    "FEMTOHERTZ",
    "FEMTOJOULE",
    "FEMTOKATAL",
    "FEMTOKELVIN",
    "FEMTOLITRE",
    "FEMTOLUMEN",
    "FEMTOLUX",
    "FEMTOMETRE",
    "FEMTOMOLE",
    "FEMTONEWTON",
    "FEMTOOHM",
    "FEMTOPASCAL",
    "FEMTORADIAN",
    "FEMTOSECOND",
    "FEMTOSIEMENS",
    "FEMTOSIEVERT",
    "FEMTOSTERADIAN",
    "FEMTOTESLA",
    "FEMTOVOLT",
    "FEMTOWATT",
    "FEMTOWEBER",
    "GIGAAMPERE",
    "GIGABECQUEREL",
    "GIGACANDELA",
    "GIGACOULOMB",
    "GIGAFARAD",
    "GIGAGRAM",
    "GIGAGRAY",
    "GIGAHENRY",
    "GIGAHERTZ",
    "GIGAJOULE",
    "GIGAKATAL",
    "GIGAKELVIN",
    "GIGALITRE",
    "GIGALUMEN",
    "GIGALUX",
    "GIGAMETRE",
    "GIGAMOLE",
    "GIGANEWTON",
    "GIGAOHM",
    "GIGAPASCAL",
    "GIGASECOND",
    "GIGASIEMENS",
    "GIGASIEVERT",
    "GIGATESLA",
    "GIGAVOLT",
    "GIGAWATT",
    "GIGAWEBER",
    "GRAM",
    "HECTOAMPERE",
    "HECTOBECQUEREL",
    "HECTOCANDELA",
    "HECTOCOULOMB",
    "HECTOFARAD",
    "HECTOGRAM",
    "HECTOGRAY",
    "HECTOHENRY",
    "HECTOHERTZ",
    "HECTOJOULE",
    "HECTOKATAL",
    "HECTOKELVIN",
    "HECTOLITRE",
    "HECTOLUMEN",
    "HECTOLUX",
    "HECTOMETRE",
    "HECTOMOLE",
    "HECTONEWTON",
    "HECTOOHM",
    "HECTOPASCAL",
    "HECTOSECOND",
    "HECTOSIEMENS",
    "HECTOSIEVERT",
    "HECTOTESLA",
    "HECTOVOLT",
    "HECTOWATT",
    "HECTOWEBER",
    "HOUR",
    "KILOAMPERE",
    "KILOBECQUEREL",
    "KILOCANDELA",
    "KILOCOULOMB",
    "KILOFARAD",
    "KILOGRAY",
    "KILOHENRY",
    "KILOHERTZ",
    "KILOJOULE",
    "KILOKATAL",
    "KILOKELVIN",
    "KILOLITRE",
    "KILOLUMEN",
    "KILOLUX",
    "KILOMETRE",
    "KILOMOLE",
    "KILONEWTON",
    "KILOOHM",
    "KILOPASCAL",
    "KILOSECOND",
    "KILOSIEMENS",
    "KILOSIEVERT",
    "KILOTESLA",
    "KILOVOLT",
    "KILOWATT",
    "KILOWEBER",
    "MEGAAMPERE",
    "MEGABECQUEREL",
    "MEGACANDELA",
    "MEGACOULOMB",
    "MEGAFARAD",
    "MEGAGRAM",
    "MEGAGRAY",
    "MEGAHENRY",
    "MEGAHERTZ",
    "MEGAJOULE",
    "MEGAKATAL",
    "MEGAKELVIN",
    "MEGALITRE",
    "MEGALUMEN",
    "MEGALUX",
    "MEGAMETRE",
    "MEGAMOLE",
    "MEGANEWTON",
    "MEGAOHM",
    "MEGAPASCAL",
    "MEGASECOND",
    "MEGASIEMENS",
    "MEGASIEVERT",
    "MEGATESLA",
    "MEGAVOLT",
    "MEGAWATT",
    "MEGAWEBER",
    "MICROAMPERE",
    "MICROBECQUEREL",
    "MICROCANDELA",
    "MICROCOULOMB",
    "MICROFARAD",
    "MICROGRAM",
    "MICROGRAY",
    "MICROHENRY",
    "MICROHERTZ",
    "MICROJOULE",
    "MICROKATAL",
    "MICROKELVIN",
    "MICROLITRE",
    "MICROLUMEN",
    "MICROLUX",
    "MICROMETRE",
    "MICROMOLE",
    "MICRONEWTON",
    "MICROOHM",
    "MICROPASCAL",
    "MICRORADIAN",
    "MICROSECOND",
    "MICROSIEMENS",
    "MICROSIEVERT",
    "MICROSTERADIAN",
    "MICROTESLA",
    "MICROVOLT",
    "MICROWATT",
    "MICROWEBER",
    "MILLENNIUM",
    "MILLIAMPERE",
    "MILLIBECQUEREL",
    "MILLICANDELA",
    "MILLICOULOMB",
    "MILLIFARAD",
    "MILLIGRAM",
    "MILLIGRAY",
    "MILLIHENRY",
    "MILLIHERTZ",
    "MILLIJOULE",
    "MILLIKATAL",
    "MILLIKELVIN",
    "MILLILITRE",
    "MILLILUMEN",
    "MILLILUX",
    "MILLIMETRE",
    "MILLIMOLE",
    "MILLINEWTON",
    "MILLIOHM",
    "MILLIPASCAL",
    "MILLIRADIAN",
    "MILLISECOND",
    "MILLISIEMENS",
    "MILLISIEVERT",
    "MILLISTERADIAN",
    "MILLITESLA",
    "MILLIVOLT",
    "MILLIWATT",
    "MILLIWEBER",
    "MINUTE",
    "NANOAMPERE",
    "NANOBECQUEREL",
    "NANOCANDELA",
    "NANOCOULOMB",
    "NANOFARAD",
    "NANOGRAM",
    "NANOGRAY",
    "NANOHENRY",
    "NANOHERTZ",
    "NANOJOULE",
    "NANOKATAL",
    "NANOKELVIN",
    "NANOLITRE",
    "NANOLUMEN",
    "NANOLUX",
    "NANOMETRE",
    "NANOMOLE",
    "NANONEWTON",
    "NANOOHM",
    "NANOPASCAL",
    "NANORADIAN",
    "NANOSECOND",
    "NANOSIEMENS",
    "NANOSIEVERT",
    "NANOSTERADIAN",
    "NANOTESLA",
    "NANOVOLT",
    "NANOWATT",
    "NANOWEBER",
    "PETAAMPERE",
    "PETABECQUEREL",
    "PETACANDELA",
    "PETACOULOMB",
    "PETAFARAD",
    "PETAGRAM",
    "PETAGRAY",
    "PETAHENRY",
    "PETAHERTZ",
    "PETAJOULE",
    "PETAKATAL",
    "PETAKELVIN",
    "PETALITRE",
    "PETALUMEN",
    "PETALUX",
    "PETAMETRE",
    "PETAMOLE",
    "PETANEWTON",
    "PETAOHM",
    "PETAPASCAL",
    "PETASECOND",
    "PETASIEMENS",
    "PETASIEVERT",
    "PETATESLA",
    "PETAVOLT",
    "PETAWATT",
    "PETAWEBER",
    "PICOAMPERE",
    "PICOBECQUEREL",
    "PICOCANDELA",
    "PICOCOULOMB",
    "PICOFARAD",
    "PICOGRAM",
    "PICOGRAY",
    "PICOHENRY",
    "PICOHERTZ",
    "PICOJOULE",
    "PICOKATAL",
    "PICOKELVIN",
    "PICOLITRE",
    "PICOLUMEN",
    "PICOLUX",
    "PICOMETRE",
    "PICOMOLE",
    "PICONEWTON",
    "PICOOHM",
    "PICOPASCAL",
    "PICORADIAN",
    "PICOSECOND",
    "PICOSIEMENS",
    "PICOSIEVERT",
    "PICOSTERADIAN",
    "PICOTESLA",
    "PICOVOLT",
    "PICOWATT",
    "PICOWEBER",
    "TERAAMPERE",
    "TERABECQUEREL",
    "TERACANDELA",
    "TERACOULOMB",
    "TERAFARAD",
    "TERAGRAM",
    "TERAGRAY",
    "TERAHENRY",
    "TERAHERTZ",
    "TERAJOULE",
    "TERAKATAL",
    "TERAKELVIN",
    "TERALITRE",
    "TERALUMEN",
    "TERALUX",
    "TERAMETRE",
    "TERAMOLE",
    "TERANEWTON",
    "TERAOHM",
    "TERAPASCAL",
    "TERASECOND",
    "TERASIEMENS",
    "TERASIEVERT",
    "TERATESLA",
    "TERAVOLT",
    "TERAWATT",
    "TERAWEBER",
    "WEEK",
    "YEAR",
    "YOCTOAMPERE",
    "YOCTOBECQUEREL",
    "YOCTOCANDELA",
    "YOCTOCOULOMB",
    "YOCTOFARAD",
    "YOCTOGRAM",
    "YOCTOGRAY",
    "YOCTOHENRY",
    "YOCTOHERTZ",
    "YOCTOJOULE",
    "YOCTOKATAL",
    "YOCTOKELVIN",
    "YOCTOLITRE",
    "YOCTOLUMEN",
    "YOCTOLUX",
    "YOCTOMETRE",
    "YOCTOMOLE",
    "YOCTONEWTON",
    "YOCTOOHM",
    "YOCTOPASCAL",
    "YOCTORADIAN",
    "YOCTOSECOND",
    "YOCTOSIEMENS",
    "YOCTOSIEVERT",
    "YOCTOSTERADIAN",
    "YOCTOTESLA",
    "YOCTOVOLT",
    "YOCTOWATT",
    "YOCTOWEBER",
    "YOTTAAMPERE",
    "YOTTABECQUEREL",
    "YOTTACANDELA",
    "YOTTACOULOMB",
    "YOTTAFARAD",
    "YOTTAGRAM",
    "YOTTAGRAY",
    "YOTTAHENRY",
    "YOTTAHERTZ",
    "YOTTAJOULE",
    "YOTTAKATAL",
    "YOTTAKELVIN",
    "YOTTALITRE",
    "YOTTALUMEN",
    "YOTTALUX",
    "YOTTAMETRE",
    "YOTTAMOLE",
    "YOTTANEWTON",
    "YOTTAOHM",
    "YOTTAPASCAL",
    "YOTTASECOND",
    "YOTTASIEMENS",
    "YOTTASIEVERT",
    "YOTTATESLA",
    "YOTTAVOLT",
    "YOTTAWATT",
    "YOTTAWEBER",
    "ZEPTOAMPERE",
    "ZEPTOBECQUEREL",
    "ZEPTOCANDELA",
    "ZEPTOCOULOMB",
    "ZEPTOFARAD",
    "ZEPTOGRAM",
    "ZEPTOGRAY",
    "ZEPTOHENRY",
    "ZEPTOHERTZ",
    "ZEPTOJOULE",
    "ZEPTOKATAL",
    "ZEPTOKELVIN",
    "ZEPTOLITRE",
    "ZEPTOLUMEN",
    "ZEPTOLUX",
    "ZEPTOMETRE",
    "ZEPTOMOLE",
    "ZEPTONEWTON",
    "ZEPTOOHM",
    "ZEPTOPASCAL",
    "ZEPTORADIAN",
    "ZEPTOSECOND",
    "ZEPTOSIEMENS",
    "ZEPTOSIEVERT",
    "ZEPTOSTERADIAN",
    "ZEPTOTESLA",
    "ZEPTOVOLT",
    "ZEPTOWATT",
    "ZEPTOWEBER",
    "ZETTAAMPERE",
    "ZETTABECQUEREL",
    "ZETTACANDELA",
    "ZETTACOULOMB",
    "ZETTAFARAD",
    "ZETTAGRAM",
    "ZETTAGRAY",
    "ZETTAHENRY",
    "ZETTAHERTZ",
    "ZETTAJOULE",
    "ZETTAKATAL",
    "ZETTAKELVIN",
    "ZETTALITRE",
    "ZETTALUMEN",
    "ZETTALUX",
    "ZETTAMETRE",
    "ZETTAMOLE",
    "ZETTANEWTON",
    "ZETTAOHM",
    "ZETTAPASCAL",
    "ZETTASECOND",
    "ZETTASIEMENS",
    "ZETTASIEVERT",
    "ZETTATESLA",
    "ZETTAVOLT",
    "ZETTAWATT",
    "ZETTAWEBER",
]

YOTTAAMPERE: Final[DerivedUnit] = DerivedUnit("YA", 1e24 * AMPERE)
ZETTAAMPERE: Final[DerivedUnit] = DerivedUnit("ZA", 1e21 * AMPERE)
EXAAMPERE: Final[DerivedUnit] = DerivedUnit("EA", 1e18 * AMPERE)
PETAAMPERE: Final[DerivedUnit] = DerivedUnit("PA", 1e15 * AMPERE)
TERAAMPERE: Final[DerivedUnit] = DerivedUnit("TA", 1e12 * AMPERE)
GIGAAMPERE: Final[DerivedUnit] = DerivedUnit("GA", 1e9 * AMPERE)
MEGAAMPERE: Final[DerivedUnit] = DerivedUnit("MA", 1e6 * AMPERE)
KILOAMPERE: Final[DerivedUnit] = DerivedUnit("kA", 1000 * AMPERE)
HECTOAMPERE: Final[DerivedUnit] = DerivedUnit("hA", 100 * AMPERE)
DECAAMPERE: Final[DerivedUnit] = DerivedUnit("daA", 10 * AMPERE)
DECIAMPERE: Final[DerivedUnit] = DerivedUnit("dA", 0.1 * AMPERE)
CENTIAMPERE: Final[DerivedUnit] = DerivedUnit("cA", 0.01 * AMPERE)
MILLIAMPERE: Final[DerivedUnit] = DerivedUnit("mA", 0.001 * AMPERE)
MICROAMPERE: Final[DerivedUnit] = DerivedUnit("μA", 1e-6 * AMPERE)
NANOAMPERE: Final[DerivedUnit] = DerivedUnit("nA", 1e-9 * AMPERE)
PICOAMPERE: Final[DerivedUnit] = DerivedUnit("pA", 1e-12 * AMPERE)
FEMTOAMPERE: Final[DerivedUnit] = DerivedUnit("pA", 1e-15 * AMPERE)
ATTOAMPERE: Final[DerivedUnit] = DerivedUnit("aA", 1e-18 * AMPERE)
ZEPTOAMPERE: Final[DerivedUnit] = DerivedUnit("zA", 1e-21 * AMPERE)
YOCTOAMPERE: Final[DerivedUnit] = DerivedUnit("yA", 1e-24 * AMPERE)

YOTTABECQUEREL: Final[DerivedUnit] = DerivedUnit("YBq", 1e24 * BECQUEREL)
ZETTABECQUEREL: Final[DerivedUnit] = DerivedUnit("ZBq", 1e21 * BECQUEREL)
EXABECQUEREL: Final[DerivedUnit] = DerivedUnit("EBq", 1e18 * BECQUEREL)
PETABECQUEREL: Final[DerivedUnit] = DerivedUnit("PBq", 1e15 * BECQUEREL)
TERABECQUEREL: Final[DerivedUnit] = DerivedUnit("TBq", 1e12 * BECQUEREL)
GIGABECQUEREL: Final[DerivedUnit] = DerivedUnit("GBq", 1e9 * BECQUEREL)
MEGABECQUEREL: Final[DerivedUnit] = DerivedUnit("MBq", 1e6 * BECQUEREL)
KILOBECQUEREL: Final[DerivedUnit] = DerivedUnit("kBq", 1000 * BECQUEREL)
HECTOBECQUEREL: Final[DerivedUnit] = DerivedUnit("hBq", 100 * BECQUEREL)
DECABECQUEREL: Final[DerivedUnit] = DerivedUnit("daBq", 10 * BECQUEREL)
DECIBECQUEREL: Final[DerivedUnit] = DerivedUnit("dBq", 0.1 * BECQUEREL)
CENTIBECQUEREL: Final[DerivedUnit] = DerivedUnit("cBq", 0.01 * BECQUEREL)
MILLIBECQUEREL: Final[DerivedUnit] = DerivedUnit("mBq", 0.001 * BECQUEREL)
MICROBECQUEREL: Final[DerivedUnit] = DerivedUnit("μBq", 1e-6 * BECQUEREL)
NANOBECQUEREL: Final[DerivedUnit] = DerivedUnit("nBq", 1e-9 * BECQUEREL)
PICOBECQUEREL: Final[DerivedUnit] = DerivedUnit("pBq", 1e-12 * BECQUEREL)
FEMTOBECQUEREL: Final[DerivedUnit] = DerivedUnit("pBq", 1e-15 * BECQUEREL)
ATTOBECQUEREL: Final[DerivedUnit] = DerivedUnit("aBq", 1e-18 * BECQUEREL)
ZEPTOBECQUEREL: Final[DerivedUnit] = DerivedUnit("zBq", 1e-21 * BECQUEREL)
YOCTOBECQUEREL: Final[DerivedUnit] = DerivedUnit("yBq", 1e-24 * BECQUEREL)

YOTTACANDELA: Final[DerivedUnit] = DerivedUnit("Ycd", 1e24 * CANDELA)
ZETTACANDELA: Final[DerivedUnit] = DerivedUnit("Zcd", 1e21 * CANDELA)
EXACANDELA: Final[DerivedUnit] = DerivedUnit("Ecd", 1e18 * CANDELA)
PETACANDELA: Final[DerivedUnit] = DerivedUnit("Pcd", 1e15 * CANDELA)
TERACANDELA: Final[DerivedUnit] = DerivedUnit("Tcd", 1e12 * CANDELA)
GIGACANDELA: Final[DerivedUnit] = DerivedUnit("Gcd", 1e9 * CANDELA)
MEGACANDELA: Final[DerivedUnit] = DerivedUnit("Mcd", 1e6 * CANDELA)
KILOCANDELA: Final[DerivedUnit] = DerivedUnit("kcd", 1000 * CANDELA)
HECTOCANDELA: Final[DerivedUnit] = DerivedUnit("hcd", 100 * CANDELA)
DECACANDELA: Final[DerivedUnit] = DerivedUnit("dacd", 10 * CANDELA)
DECICANDELA: Final[DerivedUnit] = DerivedUnit("dcd", 0.1 * CANDELA)
CENTICANDELA: Final[DerivedUnit] = DerivedUnit("ccd", 0.01 * CANDELA)
MILLICANDELA: Final[DerivedUnit] = DerivedUnit("mcd", 0.001 * CANDELA)
MICROCANDELA: Final[DerivedUnit] = DerivedUnit("μcd", 1e-6 * CANDELA)
NANOCANDELA: Final[DerivedUnit] = DerivedUnit("ncd", 1e-9 * CANDELA)
PICOCANDELA: Final[DerivedUnit] = DerivedUnit("pcd", 1e-12 * CANDELA)
FEMTOCANDELA: Final[DerivedUnit] = DerivedUnit("pcd", 1e-15 * CANDELA)
ATTOCANDELA: Final[DerivedUnit] = DerivedUnit("acd", 1e-18 * CANDELA)
ZEPTOCANDELA: Final[DerivedUnit] = DerivedUnit("zcd", 1e-21 * CANDELA)
YOCTOCANDELA: Final[DerivedUnit] = DerivedUnit("ycd", 1e-24 * CANDELA)

YOTTACOULOMB: Final[DerivedUnit] = DerivedUnit("YC", 1e24 * COULOMB)
ZETTACOULOMB: Final[DerivedUnit] = DerivedUnit("ZC", 1e21 * COULOMB)
EXACOULOMB: Final[DerivedUnit] = DerivedUnit("EC", 1e18 * COULOMB)
PETACOULOMB: Final[DerivedUnit] = DerivedUnit("PC", 1e15 * COULOMB)
TERACOULOMB: Final[DerivedUnit] = DerivedUnit("TC", 1e12 * COULOMB)
GIGACOULOMB: Final[DerivedUnit] = DerivedUnit("GC", 1e9 * COULOMB)
MEGACOULOMB: Final[DerivedUnit] = DerivedUnit("MC", 1e6 * COULOMB)
KILOCOULOMB: Final[DerivedUnit] = DerivedUnit("kC", 1000 * COULOMB)
HECTOCOULOMB: Final[DerivedUnit] = DerivedUnit("hC", 100 * COULOMB)
DECACOULOMB: Final[DerivedUnit] = DerivedUnit("daC", 10 * COULOMB)
DECICOULOMB: Final[DerivedUnit] = DerivedUnit("dC", 0.1 * COULOMB)
CENTICOULOMB: Final[DerivedUnit] = DerivedUnit("cC", 0.01 * COULOMB)
MILLICOULOMB: Final[DerivedUnit] = DerivedUnit("mC", 0.001 * COULOMB)
MICROCOULOMB: Final[DerivedUnit] = DerivedUnit("μC", 1e-6 * COULOMB)
NANOCOULOMB: Final[DerivedUnit] = DerivedUnit("nC", 1e-9 * COULOMB)
PICOCOULOMB: Final[DerivedUnit] = DerivedUnit("pC", 1e-12 * COULOMB)
FEMTOCOULOMB: Final[DerivedUnit] = DerivedUnit("pC", 1e-15 * COULOMB)
ATTOCOULOMB: Final[DerivedUnit] = DerivedUnit("aC", 1e-18 * COULOMB)
ZEPTOCOULOMB: Final[DerivedUnit] = DerivedUnit("zC", 1e-21 * COULOMB)
YOCTOCOULOMB: Final[DerivedUnit] = DerivedUnit("yC", 1e-24 * COULOMB)

YOTTAFARAD: Final[DerivedUnit] = DerivedUnit("YF", 1e24 * FARAD)
ZETTAFARAD: Final[DerivedUnit] = DerivedUnit("ZF", 1e21 * FARAD)
EXAFARAD: Final[DerivedUnit] = DerivedUnit("EF", 1e18 * FARAD)
PETAFARAD: Final[DerivedUnit] = DerivedUnit("PF", 1e15 * FARAD)
TERAFARAD: Final[DerivedUnit] = DerivedUnit("TF", 1e12 * FARAD)
GIGAFARAD: Final[DerivedUnit] = DerivedUnit("GF", 1e9 * FARAD)
MEGAFARAD: Final[DerivedUnit] = DerivedUnit("MF", 1e6 * FARAD)
KILOFARAD: Final[DerivedUnit] = DerivedUnit("kF", 1000 * FARAD)
HECTOFARAD: Final[DerivedUnit] = DerivedUnit("hF", 100 * FARAD)
DECAFARAD: Final[DerivedUnit] = DerivedUnit("daF", 10 * FARAD)
DECIFARAD: Final[DerivedUnit] = DerivedUnit("dF", 0.1 * FARAD)
CENTIFARAD: Final[DerivedUnit] = DerivedUnit("cF", 0.01 * FARAD)
MILLIFARAD: Final[DerivedUnit] = DerivedUnit("mF", 0.001 * FARAD)
MICROFARAD: Final[DerivedUnit] = DerivedUnit("μF", 1e-6 * FARAD)
NANOFARAD: Final[DerivedUnit] = DerivedUnit("nF", 1e-9 * FARAD)
PICOFARAD: Final[DerivedUnit] = DerivedUnit("pF", 1e-12 * FARAD)
FEMTOFARAD: Final[DerivedUnit] = DerivedUnit("pF", 1e-15 * FARAD)
ATTOFARAD: Final[DerivedUnit] = DerivedUnit("aF", 1e-18 * FARAD)
ZEPTOFARAD: Final[DerivedUnit] = DerivedUnit("zF", 1e-21 * FARAD)
YOCTOFARAD: Final[DerivedUnit] = DerivedUnit("yF", 1e-24 * FARAD)

YOTTAGRAY: Final[DerivedUnit] = DerivedUnit("YGy", 1e24 * GRAY)
ZETTAGRAY: Final[DerivedUnit] = DerivedUnit("ZGy", 1e21 * GRAY)
EXAGRAY: Final[DerivedUnit] = DerivedUnit("EGy", 1e18 * GRAY)
PETAGRAY: Final[DerivedUnit] = DerivedUnit("PGy", 1e15 * GRAY)
TERAGRAY: Final[DerivedUnit] = DerivedUnit("TGy", 1e12 * GRAY)
GIGAGRAY: Final[DerivedUnit] = DerivedUnit("GGy", 1e9 * GRAY)
MEGAGRAY: Final[DerivedUnit] = DerivedUnit("MGy", 1e6 * GRAY)
KILOGRAY: Final[DerivedUnit] = DerivedUnit("kGy", 1000 * GRAY)
HECTOGRAY: Final[DerivedUnit] = DerivedUnit("hGy", 100 * GRAY)
DECAGRAY: Final[DerivedUnit] = DerivedUnit("daGy", 10 * GRAY)
DECIGRAY: Final[DerivedUnit] = DerivedUnit("dGy", 0.1 * GRAY)
CENTIGRAY: Final[DerivedUnit] = DerivedUnit("cGy", 0.01 * GRAY)
MILLIGRAY: Final[DerivedUnit] = DerivedUnit("mGy", 0.001 * GRAY)
MICROGRAY: Final[DerivedUnit] = DerivedUnit("μGy", 1e-6 * GRAY)
NANOGRAY: Final[DerivedUnit] = DerivedUnit("nGy", 1e-9 * GRAY)
PICOGRAY: Final[DerivedUnit] = DerivedUnit("pGy", 1e-12 * GRAY)
FEMTOGRAY: Final[DerivedUnit] = DerivedUnit("pGy", 1e-15 * GRAY)
ATTOGRAY: Final[DerivedUnit] = DerivedUnit("aGy", 1e-18 * GRAY)
ZEPTOGRAY: Final[DerivedUnit] = DerivedUnit("zGy", 1e-21 * GRAY)
YOCTOGRAY: Final[DerivedUnit] = DerivedUnit("yGy", 1e-24 * GRAY)

YOTTAHENRY: Final[DerivedUnit] = DerivedUnit("YH", 1e24 * HENRY)
ZETTAHENRY: Final[DerivedUnit] = DerivedUnit("ZH", 1e21 * HENRY)
EXAHENRY: Final[DerivedUnit] = DerivedUnit("EH", 1e18 * HENRY)
PETAHENRY: Final[DerivedUnit] = DerivedUnit("PH", 1e15 * HENRY)
TERAHENRY: Final[DerivedUnit] = DerivedUnit("TH", 1e12 * HENRY)
GIGAHENRY: Final[DerivedUnit] = DerivedUnit("GH", 1e9 * HENRY)
MEGAHENRY: Final[DerivedUnit] = DerivedUnit("MH", 1e6 * HENRY)
KILOHENRY: Final[DerivedUnit] = DerivedUnit("kH", 1000 * HENRY)
HECTOHENRY: Final[DerivedUnit] = DerivedUnit("hH", 100 * HENRY)
DECAHENRY: Final[DerivedUnit] = DerivedUnit("daH", 10 * HENRY)
DECIHENRY: Final[DerivedUnit] = DerivedUnit("dH", 0.1 * HENRY)
CENTIHENRY: Final[DerivedUnit] = DerivedUnit("cH", 0.01 * HENRY)
MILLIHENRY: Final[DerivedUnit] = DerivedUnit("mH", 0.001 * HENRY)
MICROHENRY: Final[DerivedUnit] = DerivedUnit("μH", 1e-6 * HENRY)
NANOHENRY: Final[DerivedUnit] = DerivedUnit("nH", 1e-9 * HENRY)
PICOHENRY: Final[DerivedUnit] = DerivedUnit("pH", 1e-12 * HENRY)
FEMTOHENRY: Final[DerivedUnit] = DerivedUnit("pH", 1e-15 * HENRY)
ATTOHENRY: Final[DerivedUnit] = DerivedUnit("aH", 1e-18 * HENRY)
ZEPTOHENRY: Final[DerivedUnit] = DerivedUnit("zH", 1e-21 * HENRY)
YOCTOHENRY: Final[DerivedUnit] = DerivedUnit("yH", 1e-24 * HENRY)

YOTTAHERTZ: Final[DerivedUnit] = DerivedUnit("YHz", 1e24 * HERTZ)
ZETTAHERTZ: Final[DerivedUnit] = DerivedUnit("ZHz", 1e21 * HERTZ)
EXAHERTZ: Final[DerivedUnit] = DerivedUnit("EHz", 1e18 * HERTZ)
PETAHERTZ: Final[DerivedUnit] = DerivedUnit("PHz", 1e15 * HERTZ)
TERAHERTZ: Final[DerivedUnit] = DerivedUnit("THz", 1e12 * HERTZ)
GIGAHERTZ: Final[DerivedUnit] = DerivedUnit("GHz", 1e9 * HERTZ)
MEGAHERTZ: Final[DerivedUnit] = DerivedUnit("MHz", 1e6 * HERTZ)
KILOHERTZ: Final[DerivedUnit] = DerivedUnit("kHz", 1000 * HERTZ)
HECTOHERTZ: Final[DerivedUnit] = DerivedUnit("hHz", 100 * HERTZ)
DECAHERTZ: Final[DerivedUnit] = DerivedUnit("daHz", 10 * HERTZ)
DECIHERTZ: Final[DerivedUnit] = DerivedUnit("dHz", 0.1 * HERTZ)
CENTIHERTZ: Final[DerivedUnit] = DerivedUnit("cHz", 0.01 * HERTZ)
MILLIHERTZ: Final[DerivedUnit] = DerivedUnit("mHz", 0.001 * HERTZ)
MICROHERTZ: Final[DerivedUnit] = DerivedUnit("μHz", 1e-6 * HERTZ)
NANOHERTZ: Final[DerivedUnit] = DerivedUnit("nHz", 1e-9 * HERTZ)
PICOHERTZ: Final[DerivedUnit] = DerivedUnit("pHz", 1e-12 * HERTZ)
FEMTOHERTZ: Final[DerivedUnit] = DerivedUnit("pHz", 1e-15 * HERTZ)
ATTOHERTZ: Final[DerivedUnit] = DerivedUnit("aHz", 1e-18 * HERTZ)
ZEPTOHERTZ: Final[DerivedUnit] = DerivedUnit("zHz", 1e-21 * HERTZ)
YOCTOHERTZ: Final[DerivedUnit] = DerivedUnit("yHz", 1e-24 * HERTZ)

YOTTAJOULE: Final[DerivedUnit] = DerivedUnit("YJ", 1e24 * JOULE)
ZETTAJOULE: Final[DerivedUnit] = DerivedUnit("ZJ", 1e21 * JOULE)
EXAJOULE: Final[DerivedUnit] = DerivedUnit("EJ", 1e18 * JOULE)
PETAJOULE: Final[DerivedUnit] = DerivedUnit("PJ", 1e15 * JOULE)
TERAJOULE: Final[DerivedUnit] = DerivedUnit("TJ", 1e12 * JOULE)
GIGAJOULE: Final[DerivedUnit] = DerivedUnit("GJ", 1e9 * JOULE)
MEGAJOULE: Final[DerivedUnit] = DerivedUnit("MJ", 1e6 * JOULE)
KILOJOULE: Final[DerivedUnit] = DerivedUnit("kJ", 1000 * JOULE)
HECTOJOULE: Final[DerivedUnit] = DerivedUnit("hJ", 100 * JOULE)
DECAJOULE: Final[DerivedUnit] = DerivedUnit("daJ", 10 * JOULE)
DECIJOULE: Final[DerivedUnit] = DerivedUnit("dJ", 0.1 * JOULE)
CENTIJOULE: Final[DerivedUnit] = DerivedUnit("cJ", 0.01 * JOULE)
MILLIJOULE: Final[DerivedUnit] = DerivedUnit("mJ", 0.001 * JOULE)
MICROJOULE: Final[DerivedUnit] = DerivedUnit("μJ", 1e-6 * JOULE)
NANOJOULE: Final[DerivedUnit] = DerivedUnit("nJ", 1e-9 * JOULE)
PICOJOULE: Final[DerivedUnit] = DerivedUnit("pJ", 1e-12 * JOULE)
FEMTOJOULE: Final[DerivedUnit] = DerivedUnit("pJ", 1e-15 * JOULE)
ATTOJOULE: Final[DerivedUnit] = DerivedUnit("aJ", 1e-18 * JOULE)
ZEPTOJOULE: Final[DerivedUnit] = DerivedUnit("zJ", 1e-21 * JOULE)
YOCTOJOULE: Final[DerivedUnit] = DerivedUnit("yJ", 1e-24 * JOULE)

YOTTAKATAL: Final[DerivedUnit] = DerivedUnit("Ykat", 1e24 * KATAL)
ZETTAKATAL: Final[DerivedUnit] = DerivedUnit("Zkat", 1e21 * KATAL)
EXAKATAL: Final[DerivedUnit] = DerivedUnit("Ekat", 1e18 * KATAL)
PETAKATAL: Final[DerivedUnit] = DerivedUnit("Pkat", 1e15 * KATAL)
TERAKATAL: Final[DerivedUnit] = DerivedUnit("Tkat", 1e12 * KATAL)
GIGAKATAL: Final[DerivedUnit] = DerivedUnit("Gkat", 1e9 * KATAL)
MEGAKATAL: Final[DerivedUnit] = DerivedUnit("Mkat", 1e6 * KATAL)
KILOKATAL: Final[DerivedUnit] = DerivedUnit("kkat", 1000 * KATAL)
HECTOKATAL: Final[DerivedUnit] = DerivedUnit("hkat", 100 * KATAL)
DECAKATAL: Final[DerivedUnit] = DerivedUnit("dakat", 10 * KATAL)
DECIKATAL: Final[DerivedUnit] = DerivedUnit("dkat", 0.1 * KATAL)
CENTIKATAL: Final[DerivedUnit] = DerivedUnit("ckat", 0.01 * KATAL)
MILLIKATAL: Final[DerivedUnit] = DerivedUnit("mkat", 0.001 * KATAL)
MICROKATAL: Final[DerivedUnit] = DerivedUnit("μkat", 1e-6 * KATAL)
NANOKATAL: Final[DerivedUnit] = DerivedUnit("nkat", 1e-9 * KATAL)
PICOKATAL: Final[DerivedUnit] = DerivedUnit("pkat", 1e-12 * KATAL)
FEMTOKATAL: Final[DerivedUnit] = DerivedUnit("pkat", 1e-15 * KATAL)
ATTOKATAL: Final[DerivedUnit] = DerivedUnit("akat", 1e-18 * KATAL)
ZEPTOKATAL: Final[DerivedUnit] = DerivedUnit("zkat", 1e-21 * KATAL)
YOCTOKATAL: Final[DerivedUnit] = DerivedUnit("ykat", 1e-24 * KATAL)

YOTTAKELVIN: Final[DerivedUnit] = DerivedUnit("YK", 1e24 * KELVIN)
ZETTAKELVIN: Final[DerivedUnit] = DerivedUnit("ZK", 1e21 * KELVIN)
EXAKELVIN: Final[DerivedUnit] = DerivedUnit("EK", 1e18 * KELVIN)
PETAKELVIN: Final[DerivedUnit] = DerivedUnit("PK", 1e15 * KELVIN)
TERAKELVIN: Final[DerivedUnit] = DerivedUnit("TK", 1e12 * KELVIN)
GIGAKELVIN: Final[DerivedUnit] = DerivedUnit("GK", 1e9 * KELVIN)
MEGAKELVIN: Final[DerivedUnit] = DerivedUnit("MK", 1e6 * KELVIN)
KILOKELVIN: Final[DerivedUnit] = DerivedUnit("kK", 1000 * KELVIN)
HECTOKELVIN: Final[DerivedUnit] = DerivedUnit("hK", 100 * KELVIN)
DECAKELVIN: Final[DerivedUnit] = DerivedUnit("daK", 10 * KELVIN)
DECIKELVIN: Final[DerivedUnit] = DerivedUnit("dK", 0.1 * KELVIN)
CENTIKELVIN: Final[DerivedUnit] = DerivedUnit("cK", 0.01 * KELVIN)
MILLIKELVIN: Final[DerivedUnit] = DerivedUnit("mK", 0.001 * KELVIN)
MICROKELVIN: Final[DerivedUnit] = DerivedUnit("μK", 1e-6 * KELVIN)
NANOKELVIN: Final[DerivedUnit] = DerivedUnit("nK", 1e-9 * KELVIN)
PICOKELVIN: Final[DerivedUnit] = DerivedUnit("pK", 1e-12 * KELVIN)
FEMTOKELVIN: Final[DerivedUnit] = DerivedUnit("pK", 1e-15 * KELVIN)
ATTOKELVIN: Final[DerivedUnit] = DerivedUnit("aK", 1e-18 * KELVIN)
ZEPTOKELVIN: Final[DerivedUnit] = DerivedUnit("zK", 1e-21 * KELVIN)
YOCTOKELVIN: Final[DerivedUnit] = DerivedUnit("yK", 1e-24 * KELVIN)

GRAM: Final[DerivedUnit] = DerivedUnit("g", 0.001 * KILOGRAM)

YOTTAGRAM: Final[DerivedUnit] = DerivedUnit("Yg", 1e24 * GRAM)
ZETTAGRAM: Final[DerivedUnit] = DerivedUnit("Zg", 1e21 * GRAM)
EXAGRAM: Final[DerivedUnit] = DerivedUnit("Eg", 1e18 * GRAM)
PETAGRAM: Final[DerivedUnit] = DerivedUnit("Pg", 1e15 * GRAM)
TERAGRAM: Final[DerivedUnit] = DerivedUnit("Tg", 1e12 * GRAM)
GIGAGRAM: Final[DerivedUnit] = DerivedUnit("Gg", 1e9 * GRAM)
MEGAGRAM: Final[DerivedUnit] = DerivedUnit("Mg", 1e6 * GRAM)
HECTOGRAM: Final[DerivedUnit] = DerivedUnit("hg", 100 * GRAM)
DECAGRAM: Final[DerivedUnit] = DerivedUnit("dag", 10 * GRAM)
DECIGRAM: Final[DerivedUnit] = DerivedUnit("dg", 0.1 * GRAM)
CENTIGRAM: Final[DerivedUnit] = DerivedUnit("cg", 0.01 * GRAM)
MILLIGRAM: Final[DerivedUnit] = DerivedUnit("mg", 0.001 * GRAM)
MICROGRAM: Final[DerivedUnit] = DerivedUnit("μg", 1e-6 * GRAM)
NANOGRAM: Final[DerivedUnit] = DerivedUnit("ng", 1e-9 * GRAM)
PICOGRAM: Final[DerivedUnit] = DerivedUnit("pg", 1e-12 * GRAM)
FEMTOGRAM: Final[DerivedUnit] = DerivedUnit("pg", 1e-15 * GRAM)
ATTOGRAM: Final[DerivedUnit] = DerivedUnit("ag", 1e-18 * GRAM)
ZEPTOGRAM: Final[DerivedUnit] = DerivedUnit("zg", 1e-21 * GRAM)
YOCTOGRAM: Final[DerivedUnit] = DerivedUnit("yg", 1e-24 * GRAM)

YOTTALITRE: Final[DerivedUnit] = DerivedUnit("YL", 1e24 * LITRE)
ZETTALITRE: Final[DerivedUnit] = DerivedUnit("ZL", 1e21 * LITRE)
EXALITRE: Final[DerivedUnit] = DerivedUnit("EL", 1e18 * LITRE)
PETALITRE: Final[DerivedUnit] = DerivedUnit("PL", 1e15 * LITRE)
TERALITRE: Final[DerivedUnit] = DerivedUnit("TL", 1e12 * LITRE)
GIGALITRE: Final[DerivedUnit] = DerivedUnit("GL", 1e9 * LITRE)
MEGALITRE: Final[DerivedUnit] = DerivedUnit("ML", 1e6 * LITRE)
KILOLITRE: Final[DerivedUnit] = DerivedUnit("kL", 1000 * LITRE)
HECTOLITRE: Final[DerivedUnit] = DerivedUnit("hL", 100 * LITRE)
DECALITRE: Final[DerivedUnit] = DerivedUnit("daL", 10 * LITRE)
DECILITRE: Final[DerivedUnit] = DerivedUnit("dL", 0.1 * LITRE)
CENTILITRE: Final[DerivedUnit] = DerivedUnit("cL", 0.01 * LITRE)
MILLILITRE: Final[DerivedUnit] = DerivedUnit("mL", 0.001 * LITRE)
MICROLITRE: Final[DerivedUnit] = DerivedUnit("μL", 1e-6 * LITRE)
NANOLITRE: Final[DerivedUnit] = DerivedUnit("nL", 1e-9 * LITRE)
PICOLITRE: Final[DerivedUnit] = DerivedUnit("pL", 1e-12 * LITRE)
FEMTOLITRE: Final[DerivedUnit] = DerivedUnit("pL", 1e-15 * LITRE)
ATTOLITRE: Final[DerivedUnit] = DerivedUnit("aL", 1e-18 * LITRE)
ZEPTOLITRE: Final[DerivedUnit] = DerivedUnit("zL", 1e-21 * LITRE)
YOCTOLITRE: Final[DerivedUnit] = DerivedUnit("yL", 1e-24 * LITRE)

YOTTALUMEN: Final[DerivedUnit] = DerivedUnit("Ylm", 1e24 * LUMEN)
ZETTALUMEN: Final[DerivedUnit] = DerivedUnit("Zlm", 1e21 * LUMEN)
EXALUMEN: Final[DerivedUnit] = DerivedUnit("Elm", 1e18 * LUMEN)
PETALUMEN: Final[DerivedUnit] = DerivedUnit("Plm", 1e15 * LUMEN)
TERALUMEN: Final[DerivedUnit] = DerivedUnit("Tlm", 1e12 * LUMEN)
GIGALUMEN: Final[DerivedUnit] = DerivedUnit("Glm", 1e9 * LUMEN)
MEGALUMEN: Final[DerivedUnit] = DerivedUnit("Mlm", 1e6 * LUMEN)
KILOLUMEN: Final[DerivedUnit] = DerivedUnit("klm", 1000 * LUMEN)
HECTOLUMEN: Final[DerivedUnit] = DerivedUnit("hlm", 100 * LUMEN)
DECALUMEN: Final[DerivedUnit] = DerivedUnit("dalm", 10 * LUMEN)
DECILUMEN: Final[DerivedUnit] = DerivedUnit("dlm", 0.1 * LUMEN)
CENTILUMEN: Final[DerivedUnit] = DerivedUnit("clm", 0.01 * LUMEN)
MILLILUMEN: Final[DerivedUnit] = DerivedUnit("mlm", 0.001 * LUMEN)
MICROLUMEN: Final[DerivedUnit] = DerivedUnit("μlm", 1e-6 * LUMEN)
NANOLUMEN: Final[DerivedUnit] = DerivedUnit("nlm", 1e-9 * LUMEN)
PICOLUMEN: Final[DerivedUnit] = DerivedUnit("plm", 1e-12 * LUMEN)
FEMTOLUMEN: Final[DerivedUnit] = DerivedUnit("plm", 1e-15 * LUMEN)
ATTOLUMEN: Final[DerivedUnit] = DerivedUnit("alm", 1e-18 * LUMEN)
ZEPTOLUMEN: Final[DerivedUnit] = DerivedUnit("zlm", 1e-21 * LUMEN)
YOCTOLUMEN: Final[DerivedUnit] = DerivedUnit("ylm", 1e-24 * LUMEN)

YOTTALUX: Final[DerivedUnit] = DerivedUnit("Ylx", 1e24 * LUX)
ZETTALUX: Final[DerivedUnit] = DerivedUnit("Zlx", 1e21 * LUX)
EXALUX: Final[DerivedUnit] = DerivedUnit("Elx", 1e18 * LUX)
PETALUX: Final[DerivedUnit] = DerivedUnit("Plx", 1e15 * LUX)
TERALUX: Final[DerivedUnit] = DerivedUnit("Tlx", 1e12 * LUX)
GIGALUX: Final[DerivedUnit] = DerivedUnit("Glx", 1e9 * LUX)
MEGALUX: Final[DerivedUnit] = DerivedUnit("Mlx", 1e6 * LUX)
KILOLUX: Final[DerivedUnit] = DerivedUnit("klx", 1000 * LUX)
HECTOLUX: Final[DerivedUnit] = DerivedUnit("hlx", 100 * LUX)
DECALUX: Final[DerivedUnit] = DerivedUnit("dalx", 10 * LUX)
DECILUX: Final[DerivedUnit] = DerivedUnit("dlx", 0.1 * LUX)
CENTILUX: Final[DerivedUnit] = DerivedUnit("clx", 0.01 * LUX)
MILLILUX: Final[DerivedUnit] = DerivedUnit("mlx", 0.001 * LUX)
MICROLUX: Final[DerivedUnit] = DerivedUnit("μlx", 1e-6 * LUX)
NANOLUX: Final[DerivedUnit] = DerivedUnit("nlx", 1e-9 * LUX)
PICOLUX: Final[DerivedUnit] = DerivedUnit("plx", 1e-12 * LUX)
FEMTOLUX: Final[DerivedUnit] = DerivedUnit("plx", 1e-15 * LUX)
ATTOLUX: Final[DerivedUnit] = DerivedUnit("alx", 1e-18 * LUX)
ZEPTOLUX: Final[DerivedUnit] = DerivedUnit("zlx", 1e-21 * LUX)
YOCTOLUX: Final[DerivedUnit] = DerivedUnit("ylx", 1e-24 * LUX)

YOTTAMETRE: Final[DerivedUnit] = DerivedUnit("Ym", 1e24 * METRE)
ZETTAMETRE: Final[DerivedUnit] = DerivedUnit("Zm", 1e21 * METRE)
EXAMETRE: Final[DerivedUnit] = DerivedUnit("Em", 1e18 * METRE)
PETAMETRE: Final[DerivedUnit] = DerivedUnit("Pm", 1e15 * METRE)
TERAMETRE: Final[DerivedUnit] = DerivedUnit("Tm", 1e12 * METRE)
GIGAMETRE: Final[DerivedUnit] = DerivedUnit("Gm", 1e9 * METRE)
MEGAMETRE: Final[DerivedUnit] = DerivedUnit("Mm", 1e6 * METRE)
KILOMETRE: Final[DerivedUnit] = DerivedUnit("km", 1000 * METRE)
HECTOMETRE: Final[DerivedUnit] = DerivedUnit("hm", 100 * METRE)
DECAMETRE: Final[DerivedUnit] = DerivedUnit("dam", 10 * METRE)
DECIMETRE: Final[DerivedUnit] = DerivedUnit("dm", 0.1 * METRE)
CENTIMETRE: Final[DerivedUnit] = DerivedUnit("cm", 0.01 * METRE)
MILLIMETRE: Final[DerivedUnit] = DerivedUnit("mm", 0.001 * METRE)
MICROMETRE: Final[DerivedUnit] = DerivedUnit("μm", 1e-6 * METRE)
NANOMETRE: Final[DerivedUnit] = DerivedUnit("nm", 1e-9 * METRE)
PICOMETRE: Final[DerivedUnit] = DerivedUnit("pm", 1e-12 * METRE)
FEMTOMETRE: Final[DerivedUnit] = DerivedUnit("pm", 1e-15 * METRE)
ATTOMETRE: Final[DerivedUnit] = DerivedUnit("am", 1e-18 * METRE)
ZEPTOMETRE: Final[DerivedUnit] = DerivedUnit("zm", 1e-21 * METRE)
YOCTOMETRE: Final[DerivedUnit] = DerivedUnit("ym", 1e-24 * METRE)

YOTTAMOLE: Final[DerivedUnit] = DerivedUnit("Ymol", 1e24 * MOLE)
ZETTAMOLE: Final[DerivedUnit] = DerivedUnit("Zmol", 1e21 * MOLE)
EXAMOLE: Final[DerivedUnit] = DerivedUnit("Emol", 1e18 * MOLE)
PETAMOLE: Final[DerivedUnit] = DerivedUnit("Pmol", 1e15 * MOLE)
TERAMOLE: Final[DerivedUnit] = DerivedUnit("Tmol", 1e12 * MOLE)
GIGAMOLE: Final[DerivedUnit] = DerivedUnit("Gmol", 1e9 * MOLE)
MEGAMOLE: Final[DerivedUnit] = DerivedUnit("Mmol", 1e6 * MOLE)
KILOMOLE: Final[DerivedUnit] = DerivedUnit("kmol", 1000 * MOLE)
HECTOMOLE: Final[DerivedUnit] = DerivedUnit("hmol", 100 * MOLE)
DECAMOLE: Final[DerivedUnit] = DerivedUnit("damol", 10 * MOLE)
DECIMOLE: Final[DerivedUnit] = DerivedUnit("dmol", 0.1 * MOLE)
CENTIMOLE: Final[DerivedUnit] = DerivedUnit("cmol", 0.01 * MOLE)
MILLIMOLE: Final[DerivedUnit] = DerivedUnit("mmol", 0.001 * MOLE)
MICROMOLE: Final[DerivedUnit] = DerivedUnit("μmol", 1e-6 * MOLE)
NANOMOLE: Final[DerivedUnit] = DerivedUnit("nmol", 1e-9 * MOLE)
PICOMOLE: Final[DerivedUnit] = DerivedUnit("pmol", 1e-12 * MOLE)
FEMTOMOLE: Final[DerivedUnit] = DerivedUnit("pmol", 1e-15 * MOLE)
ATTOMOLE: Final[DerivedUnit] = DerivedUnit("amol", 1e-18 * MOLE)
ZEPTOMOLE: Final[DerivedUnit] = DerivedUnit("zmol", 1e-21 * MOLE)
YOCTOMOLE: Final[DerivedUnit] = DerivedUnit("ymol", 1e-24 * MOLE)

YOTTANEWTON: Final[DerivedUnit] = DerivedUnit("YN", 1e24 * NEWTON)
ZETTANEWTON: Final[DerivedUnit] = DerivedUnit("ZN", 1e21 * NEWTON)
EXANEWTON: Final[DerivedUnit] = DerivedUnit("EN", 1e18 * NEWTON)
PETANEWTON: Final[DerivedUnit] = DerivedUnit("PN", 1e15 * NEWTON)
TERANEWTON: Final[DerivedUnit] = DerivedUnit("TN", 1e12 * NEWTON)
GIGANEWTON: Final[DerivedUnit] = DerivedUnit("GN", 1e9 * NEWTON)
MEGANEWTON: Final[DerivedUnit] = DerivedUnit("MN", 1e6 * NEWTON)
KILONEWTON: Final[DerivedUnit] = DerivedUnit("kN", 1000 * NEWTON)
HECTONEWTON: Final[DerivedUnit] = DerivedUnit("hN", 100 * NEWTON)
DECANEWTON: Final[DerivedUnit] = DerivedUnit("daN", 10 * NEWTON)
DECINEWTON: Final[DerivedUnit] = DerivedUnit("dN", 0.1 * NEWTON)
CENTINEWTON: Final[DerivedUnit] = DerivedUnit("cN", 0.01 * NEWTON)
MILLINEWTON: Final[DerivedUnit] = DerivedUnit("mN", 0.001 * NEWTON)
MICRONEWTON: Final[DerivedUnit] = DerivedUnit("μN", 1e-6 * NEWTON)
NANONEWTON: Final[DerivedUnit] = DerivedUnit("nN", 1e-9 * NEWTON)
PICONEWTON: Final[DerivedUnit] = DerivedUnit("pN", 1e-12 * NEWTON)
FEMTONEWTON: Final[DerivedUnit] = DerivedUnit("pN", 1e-15 * NEWTON)
ATTONEWTON: Final[DerivedUnit] = DerivedUnit("aN", 1e-18 * NEWTON)
ZEPTONEWTON: Final[DerivedUnit] = DerivedUnit("zN", 1e-21 * NEWTON)
YOCTONEWTON: Final[DerivedUnit] = DerivedUnit("yN", 1e-24 * NEWTON)

YOTTAOHM: Final[DerivedUnit] = DerivedUnit("YΩ", 1e24 * OHM)
ZETTAOHM: Final[DerivedUnit] = DerivedUnit("ZΩ", 1e21 * OHM)
EXAOHM: Final[DerivedUnit] = DerivedUnit("EΩ", 1e18 * OHM)
PETAOHM: Final[DerivedUnit] = DerivedUnit("PΩ", 1e15 * OHM)
TERAOHM: Final[DerivedUnit] = DerivedUnit("TΩ", 1e12 * OHM)
GIGAOHM: Final[DerivedUnit] = DerivedUnit("GΩ", 1e9 * OHM)
MEGAOHM: Final[DerivedUnit] = DerivedUnit("MΩ", 1e6 * OHM)
KILOOHM: Final[DerivedUnit] = DerivedUnit("kΩ", 1000 * OHM)
HECTOOHM: Final[DerivedUnit] = DerivedUnit("hΩ", 100 * OHM)
DECAOHM: Final[DerivedUnit] = DerivedUnit("daΩ", 10 * OHM)
DECIOHM: Final[DerivedUnit] = DerivedUnit("dΩ", 0.1 * OHM)
CENTIOHM: Final[DerivedUnit] = DerivedUnit("cΩ", 0.01 * OHM)
MILLIOHM: Final[DerivedUnit] = DerivedUnit("mΩ", 0.001 * OHM)
MICROOHM: Final[DerivedUnit] = DerivedUnit("μΩ", 1e-6 * OHM)
NANOOHM: Final[DerivedUnit] = DerivedUnit("nΩ", 1e-9 * OHM)
PICOOHM: Final[DerivedUnit] = DerivedUnit("pΩ", 1e-12 * OHM)
FEMTOOHM: Final[DerivedUnit] = DerivedUnit("pΩ", 1e-15 * OHM)
ATTOOHM: Final[DerivedUnit] = DerivedUnit("aΩ", 1e-18 * OHM)
ZEPTOOHM: Final[DerivedUnit] = DerivedUnit("zΩ", 1e-21 * OHM)
YOCTOOHM: Final[DerivedUnit] = DerivedUnit("yΩ", 1e-24 * OHM)

YOTTAPASCAL: Final[DerivedUnit] = DerivedUnit("YPa", 1e24 * PASCAL)
ZETTAPASCAL: Final[DerivedUnit] = DerivedUnit("ZPa", 1e21 * PASCAL)
EXAPASCAL: Final[DerivedUnit] = DerivedUnit("EPa", 1e18 * PASCAL)
PETAPASCAL: Final[DerivedUnit] = DerivedUnit("PPa", 1e15 * PASCAL)
TERAPASCAL: Final[DerivedUnit] = DerivedUnit("TPa", 1e12 * PASCAL)
GIGAPASCAL: Final[DerivedUnit] = DerivedUnit("GPa", 1e9 * PASCAL)
MEGAPASCAL: Final[DerivedUnit] = DerivedUnit("MPa", 1e6 * PASCAL)
KILOPASCAL: Final[DerivedUnit] = DerivedUnit("kPa", 1000 * PASCAL)
HECTOPASCAL: Final[DerivedUnit] = DerivedUnit("hPa", 100 * PASCAL)
DECAPASCAL: Final[DerivedUnit] = DerivedUnit("daPa", 10 * PASCAL)
DECIPASCAL: Final[DerivedUnit] = DerivedUnit("dPa", 0.1 * PASCAL)
CENTIPASCAL: Final[DerivedUnit] = DerivedUnit("cPa", 0.01 * PASCAL)
MILLIPASCAL: Final[DerivedUnit] = DerivedUnit("mPa", 0.001 * PASCAL)
MICROPASCAL: Final[DerivedUnit] = DerivedUnit("μPa", 1e-6 * PASCAL)
NANOPASCAL: Final[DerivedUnit] = DerivedUnit("nPa", 1e-9 * PASCAL)
PICOPASCAL: Final[DerivedUnit] = DerivedUnit("pPa", 1e-12 * PASCAL)
FEMTOPASCAL: Final[DerivedUnit] = DerivedUnit("pPa", 1e-15 * PASCAL)
ATTOPASCAL: Final[DerivedUnit] = DerivedUnit("aPa", 1e-18 * PASCAL)
ZEPTOPASCAL: Final[DerivedUnit] = DerivedUnit("zPa", 1e-21 * PASCAL)
YOCTOPASCAL: Final[DerivedUnit] = DerivedUnit("yPa", 1e-24 * PASCAL)

DECIRADIAN: Final[DerivedUnit] = DerivedUnit("drad", 0.1 * RADIAN)
CENTIRADIAN: Final[DerivedUnit] = DerivedUnit("crad", 0.01 * RADIAN)
MILLIRADIAN: Final[DerivedUnit] = DerivedUnit("mrad", 0.001 * RADIAN)
MICRORADIAN: Final[DerivedUnit] = DerivedUnit("μrad", 1e-6 * RADIAN)
NANORADIAN: Final[DerivedUnit] = DerivedUnit("nrad", 1e-9 * RADIAN)
PICORADIAN: Final[DerivedUnit] = DerivedUnit("prad", 1e-12 * RADIAN)
FEMTORADIAN: Final[DerivedUnit] = DerivedUnit("prad", 1e-15 * RADIAN)
ATTORADIAN: Final[DerivedUnit] = DerivedUnit("arad", 1e-18 * RADIAN)
ZEPTORADIAN: Final[DerivedUnit] = DerivedUnit("zrad", 1e-21 * RADIAN)
YOCTORADIAN: Final[DerivedUnit] = DerivedUnit("yrad", 1e-24 * RADIAN)

DEGREE: Final[DerivedUnit] = DerivedUnit("°", radians(1.0) * RADIAN)
ARC_MINUTE: Final[DerivedUnit] = DerivedUnit("'", DEGREE / 60)
ARC_SECOND: Final[DerivedUnit] = DerivedUnit('"', ARC_MINUTE / 60)

YOTTASECOND: Final[DerivedUnit] = DerivedUnit("Ys", 1e24 * SECOND)
ZETTASECOND: Final[DerivedUnit] = DerivedUnit("Zs", 1e21 * SECOND)
EXASECOND: Final[DerivedUnit] = DerivedUnit("Es", 1e18 * SECOND)
PETASECOND: Final[DerivedUnit] = DerivedUnit("Ps", 1e15 * SECOND)
TERASECOND: Final[DerivedUnit] = DerivedUnit("Ts", 1e12 * SECOND)
GIGASECOND: Final[DerivedUnit] = DerivedUnit("Gs", 1e9 * SECOND)
MEGASECOND: Final[DerivedUnit] = DerivedUnit("Ms", 1e6 * SECOND)
KILOSECOND: Final[DerivedUnit] = DerivedUnit("ks", 1000 * SECOND)
HECTOSECOND: Final[DerivedUnit] = DerivedUnit("hs", 100 * SECOND)
DECASECOND: Final[DerivedUnit] = DerivedUnit("das", 10 * SECOND)
DECISECOND: Final[DerivedUnit] = DerivedUnit("ds", 0.1 * SECOND)
CENTISECOND: Final[DerivedUnit] = DerivedUnit("cs", 0.01 * SECOND)
MILLISECOND: Final[DerivedUnit] = DerivedUnit("ms", 0.001 * SECOND)
MICROSECOND: Final[DerivedUnit] = DerivedUnit("μs", 1e-6 * SECOND)
NANOSECOND: Final[DerivedUnit] = DerivedUnit("ns", 1e-9 * SECOND)
PICOSECOND: Final[DerivedUnit] = DerivedUnit("ps", 1e-12 * SECOND)
FEMTOSECOND: Final[DerivedUnit] = DerivedUnit("ps", 1e-15 * SECOND)
ATTOSECOND: Final[DerivedUnit] = DerivedUnit("as", 1e-18 * SECOND)
ZEPTOSECOND: Final[DerivedUnit] = DerivedUnit("zs", 1e-21 * SECOND)
YOCTOSECOND: Final[DerivedUnit] = DerivedUnit("ys", 1e-24 * SECOND)

MINUTE: Final[DerivedUnit] = DerivedUnit("min", 60 * SECOND)
HOUR: Final[DerivedUnit] = DerivedUnit("h", 60 * MINUTE)
DAY: Final[DerivedUnit] = DerivedUnit("d", 24 * HOUR)
WEEK: Final[DerivedUnit] = DerivedUnit("wk", 7 * DAY)
YEAR: Final[DerivedUnit] = DerivedUnit("y", 365.2425 * DAY)
DECADE: Final[DerivedUnit] = DerivedUnit("dec", 10 * YEAR)
CENTURY: Final[DerivedUnit] = DerivedUnit("c", 100 * YEAR)
MILLENNIUM: Final[DerivedUnit] = DerivedUnit("mil", 1000 * YEAR)

YOTTASIEMENS: Final[DerivedUnit] = DerivedUnit("YS", 1e24 * SIEMENS)
ZETTASIEMENS: Final[DerivedUnit] = DerivedUnit("ZS", 1e21 * SIEMENS)
EXASIEMENS: Final[DerivedUnit] = DerivedUnit("ES", 1e18 * SIEMENS)
PETASIEMENS: Final[DerivedUnit] = DerivedUnit("PS", 1e15 * SIEMENS)
TERASIEMENS: Final[DerivedUnit] = DerivedUnit("TS", 1e12 * SIEMENS)
GIGASIEMENS: Final[DerivedUnit] = DerivedUnit("GS", 1e9 * SIEMENS)
MEGASIEMENS: Final[DerivedUnit] = DerivedUnit("MS", 1e6 * SIEMENS)
KILOSIEMENS: Final[DerivedUnit] = DerivedUnit("kS", 1000 * SIEMENS)
HECTOSIEMENS: Final[DerivedUnit] = DerivedUnit("hS", 100 * SIEMENS)
DECASIEMENS: Final[DerivedUnit] = DerivedUnit("daS", 10 * SIEMENS)
DECISIEMENS: Final[DerivedUnit] = DerivedUnit("dS", 0.1 * SIEMENS)
CENTISIEMENS: Final[DerivedUnit] = DerivedUnit("cS", 0.01 * SIEMENS)
MILLISIEMENS: Final[DerivedUnit] = DerivedUnit("mS", 0.001 * SIEMENS)
MICROSIEMENS: Final[DerivedUnit] = DerivedUnit("μS", 1e-6 * SIEMENS)
NANOSIEMENS: Final[DerivedUnit] = DerivedUnit("nS", 1e-9 * SIEMENS)
PICOSIEMENS: Final[DerivedUnit] = DerivedUnit("pS", 1e-12 * SIEMENS)
FEMTOSIEMENS: Final[DerivedUnit] = DerivedUnit("pS", 1e-15 * SIEMENS)
ATTOSIEMENS: Final[DerivedUnit] = DerivedUnit("aS", 1e-18 * SIEMENS)
ZEPTOSIEMENS: Final[DerivedUnit] = DerivedUnit("zS", 1e-21 * SIEMENS)
YOCTOSIEMENS: Final[DerivedUnit] = DerivedUnit("yS", 1e-24 * SIEMENS)

YOTTASIEVERT: Final[DerivedUnit] = DerivedUnit("YSv", 1e24 * SIEVERT)
ZETTASIEVERT: Final[DerivedUnit] = DerivedUnit("ZSv", 1e21 * SIEVERT)
EXASIEVERT: Final[DerivedUnit] = DerivedUnit("ESv", 1e18 * SIEVERT)
PETASIEVERT: Final[DerivedUnit] = DerivedUnit("PSv", 1e15 * SIEVERT)
TERASIEVERT: Final[DerivedUnit] = DerivedUnit("TSv", 1e12 * SIEVERT)
GIGASIEVERT: Final[DerivedUnit] = DerivedUnit("GSv", 1e9 * SIEVERT)
MEGASIEVERT: Final[DerivedUnit] = DerivedUnit("MSv", 1e6 * SIEVERT)
KILOSIEVERT: Final[DerivedUnit] = DerivedUnit("kSv", 1000 * SIEVERT)
HECTOSIEVERT: Final[DerivedUnit] = DerivedUnit("hSv", 100 * SIEVERT)
DECASIEVERT: Final[DerivedUnit] = DerivedUnit("daSv", 10 * SIEVERT)
DECISIEVERT: Final[DerivedUnit] = DerivedUnit("dSv", 0.1 * SIEVERT)
CENTISIEVERT: Final[DerivedUnit] = DerivedUnit("cSv", 0.01 * SIEVERT)
MILLISIEVERT: Final[DerivedUnit] = DerivedUnit("mSv", 0.001 * SIEVERT)
MICROSIEVERT: Final[DerivedUnit] = DerivedUnit("μSv", 1e-6 * SIEVERT)
NANOSIEVERT: Final[DerivedUnit] = DerivedUnit("nSv", 1e-9 * SIEVERT)
PICOSIEVERT: Final[DerivedUnit] = DerivedUnit("pSv", 1e-12 * SIEVERT)
FEMTOSIEVERT: Final[DerivedUnit] = DerivedUnit("pSv", 1e-15 * SIEVERT)
ATTOSIEVERT: Final[DerivedUnit] = DerivedUnit("aSv", 1e-18 * SIEVERT)
ZEPTOSIEVERT: Final[DerivedUnit] = DerivedUnit("zSv", 1e-21 * SIEVERT)
YOCTOSIEVERT: Final[DerivedUnit] = DerivedUnit("ySv", 1e-24 * SIEVERT)

DECISTERADIAN: Final[DerivedUnit] = DerivedUnit("dsr", 0.1 * STERADIAN)
CENTISTERADIAN: Final[DerivedUnit] = DerivedUnit("csr", 0.01 * STERADIAN)
MILLISTERADIAN: Final[DerivedUnit] = DerivedUnit("msr", 0.001 * STERADIAN)
MICROSTERADIAN: Final[DerivedUnit] = DerivedUnit("μsr", 1e-6 * STERADIAN)
NANOSTERADIAN: Final[DerivedUnit] = DerivedUnit("nsr", 1e-9 * STERADIAN)
PICOSTERADIAN: Final[DerivedUnit] = DerivedUnit("psr", 1e-12 * STERADIAN)
FEMTOSTERADIAN: Final[DerivedUnit] = DerivedUnit("psr", 1e-15 * STERADIAN)
ATTOSTERADIAN: Final[DerivedUnit] = DerivedUnit("asr", 1e-18 * STERADIAN)
ZEPTOSTERADIAN: Final[DerivedUnit] = DerivedUnit("zsr", 1e-21 * STERADIAN)
YOCTOSTERADIAN: Final[DerivedUnit] = DerivedUnit("ysr", 1e-24 * STERADIAN)

YOTTATESLA: Final[DerivedUnit] = DerivedUnit("YT", 1e24 * TESLA)
ZETTATESLA: Final[DerivedUnit] = DerivedUnit("ZT", 1e21 * TESLA)
EXATESLA: Final[DerivedUnit] = DerivedUnit("ET", 1e18 * TESLA)
PETATESLA: Final[DerivedUnit] = DerivedUnit("PT", 1e15 * TESLA)
TERATESLA: Final[DerivedUnit] = DerivedUnit("TT", 1e12 * TESLA)
GIGATESLA: Final[DerivedUnit] = DerivedUnit("GT", 1e9 * TESLA)
MEGATESLA: Final[DerivedUnit] = DerivedUnit("MT", 1e6 * TESLA)
KILOTESLA: Final[DerivedUnit] = DerivedUnit("kT", 1000 * TESLA)
HECTOTESLA: Final[DerivedUnit] = DerivedUnit("hT", 100 * TESLA)
DECATESLA: Final[DerivedUnit] = DerivedUnit("daT", 10 * TESLA)
DECITESLA: Final[DerivedUnit] = DerivedUnit("dT", 0.1 * TESLA)
CENTITESLA: Final[DerivedUnit] = DerivedUnit("cT", 0.01 * TESLA)
MILLITESLA: Final[DerivedUnit] = DerivedUnit("mT", 0.001 * TESLA)
MICROTESLA: Final[DerivedUnit] = DerivedUnit("μT", 1e-6 * TESLA)
NANOTESLA: Final[DerivedUnit] = DerivedUnit("nT", 1e-9 * TESLA)
PICOTESLA: Final[DerivedUnit] = DerivedUnit("pT", 1e-12 * TESLA)
FEMTOTESLA: Final[DerivedUnit] = DerivedUnit("pT", 1e-15 * TESLA)
ATTOTESLA: Final[DerivedUnit] = DerivedUnit("aT", 1e-18 * TESLA)
ZEPTOTESLA: Final[DerivedUnit] = DerivedUnit("zT", 1e-21 * TESLA)
YOCTOTESLA: Final[DerivedUnit] = DerivedUnit("yT", 1e-24 * TESLA)

YOTTAVOLT: Final[DerivedUnit] = DerivedUnit("YV", 1e24 * VOLT)
ZETTAVOLT: Final[DerivedUnit] = DerivedUnit("ZV", 1e21 * VOLT)
EXAVOLT: Final[DerivedUnit] = DerivedUnit("EV", 1e18 * VOLT)
PETAVOLT: Final[DerivedUnit] = DerivedUnit("PV", 1e15 * VOLT)
TERAVOLT: Final[DerivedUnit] = DerivedUnit("TV", 1e12 * VOLT)
GIGAVOLT: Final[DerivedUnit] = DerivedUnit("GV", 1e9 * VOLT)
MEGAVOLT: Final[DerivedUnit] = DerivedUnit("MV", 1e6 * VOLT)
KILOVOLT: Final[DerivedUnit] = DerivedUnit("kV", 1000 * VOLT)
HECTOVOLT: Final[DerivedUnit] = DerivedUnit("hV", 100 * VOLT)
DECAVOLT: Final[DerivedUnit] = DerivedUnit("daV", 10 * VOLT)
DECIVOLT: Final[DerivedUnit] = DerivedUnit("dV", 0.1 * VOLT)
CENTIVOLT: Final[DerivedUnit] = DerivedUnit("cV", 0.01 * VOLT)
MILLIVOLT: Final[DerivedUnit] = DerivedUnit("mV", 0.001 * VOLT)
MICROVOLT: Final[DerivedUnit] = DerivedUnit("μV", 1e-6 * VOLT)
NANOVOLT: Final[DerivedUnit] = DerivedUnit("nV", 1e-9 * VOLT)
PICOVOLT: Final[DerivedUnit] = DerivedUnit("pV", 1e-12 * VOLT)
FEMTOVOLT: Final[DerivedUnit] = DerivedUnit("pV", 1e-15 * VOLT)
ATTOVOLT: Final[DerivedUnit] = DerivedUnit("aV", 1e-18 * VOLT)
ZEPTOVOLT: Final[DerivedUnit] = DerivedUnit("zV", 1e-21 * VOLT)
YOCTOVOLT: Final[DerivedUnit] = DerivedUnit("yV", 1e-24 * VOLT)

YOTTAWATT: Final[DerivedUnit] = DerivedUnit("YW", 1e24 * WATT)
ZETTAWATT: Final[DerivedUnit] = DerivedUnit("ZW", 1e21 * WATT)
EXAWATT: Final[DerivedUnit] = DerivedUnit("EW", 1e18 * WATT)
PETAWATT: Final[DerivedUnit] = DerivedUnit("PW", 1e15 * WATT)
TERAWATT: Final[DerivedUnit] = DerivedUnit("TW", 1e12 * WATT)
GIGAWATT: Final[DerivedUnit] = DerivedUnit("GW", 1e9 * WATT)
MEGAWATT: Final[DerivedUnit] = DerivedUnit("MW", 1e6 * WATT)
KILOWATT: Final[DerivedUnit] = DerivedUnit("kW", 1000 * WATT)
HECTOWATT: Final[DerivedUnit] = DerivedUnit("hW", 100 * WATT)
DECAWATT: Final[DerivedUnit] = DerivedUnit("daW", 10 * WATT)
DECIWATT: Final[DerivedUnit] = DerivedUnit("dW", 0.1 * WATT)
CENTIWATT: Final[DerivedUnit] = DerivedUnit("cW", 0.01 * WATT)
MILLIWATT: Final[DerivedUnit] = DerivedUnit("mW", 0.001 * WATT)
MICROWATT: Final[DerivedUnit] = DerivedUnit("μW", 1e-6 * WATT)
NANOWATT: Final[DerivedUnit] = DerivedUnit("nW", 1e-9 * WATT)
PICOWATT: Final[DerivedUnit] = DerivedUnit("pW", 1e-12 * WATT)
FEMTOWATT: Final[DerivedUnit] = DerivedUnit("pW", 1e-15 * WATT)
ATTOWATT: Final[DerivedUnit] = DerivedUnit("aW", 1e-18 * WATT)
ZEPTOWATT: Final[DerivedUnit] = DerivedUnit("zW", 1e-21 * WATT)
YOCTOWATT: Final[DerivedUnit] = DerivedUnit("yW", 1e-24 * WATT)

YOTTAWEBER: Final[DerivedUnit] = DerivedUnit("YWb", 1e24 * WEBER)
ZETTAWEBER: Final[DerivedUnit] = DerivedUnit("ZWb", 1e21 * WEBER)
EXAWEBER: Final[DerivedUnit] = DerivedUnit("EWb", 1e18 * WEBER)
PETAWEBER: Final[DerivedUnit] = DerivedUnit("PWb", 1e15 * WEBER)
TERAWEBER: Final[DerivedUnit] = DerivedUnit("TWb", 1e12 * WEBER)
GIGAWEBER: Final[DerivedUnit] = DerivedUnit("GWb", 1e9 * WEBER)
MEGAWEBER: Final[DerivedUnit] = DerivedUnit("MWb", 1e6 * WEBER)
KILOWEBER: Final[DerivedUnit] = DerivedUnit("kWb", 1000 * WEBER)
HECTOWEBER: Final[DerivedUnit] = DerivedUnit("hWb", 100 * WEBER)
DECAWEBER: Final[DerivedUnit] = DerivedUnit("daWb", 10 * WEBER)
DECIWEBER: Final[DerivedUnit] = DerivedUnit("dWb", 0.1 * WEBER)
CENTIWEBER: Final[DerivedUnit] = DerivedUnit("cWb", 0.01 * WEBER)
MILLIWEBER: Final[DerivedUnit] = DerivedUnit("mWb", 0.001 * WEBER)
MICROWEBER: Final[DerivedUnit] = DerivedUnit("μWb", 1e-6 * WEBER)
NANOWEBER: Final[DerivedUnit] = DerivedUnit("nWb", 1e-9 * WEBER)
PICOWEBER: Final[DerivedUnit] = DerivedUnit("pWb", 1e-12 * WEBER)
FEMTOWEBER: Final[DerivedUnit] = DerivedUnit("pWb", 1e-15 * WEBER)
ATTOWEBER: Final[DerivedUnit] = DerivedUnit("aWb", 1e-18 * WEBER)
ZEPTOWEBER: Final[DerivedUnit] = DerivedUnit("zWb", 1e-21 * WEBER)
YOCTOWEBER: Final[DerivedUnit] = DerivedUnit("yWb", 1e-24 * WEBER)

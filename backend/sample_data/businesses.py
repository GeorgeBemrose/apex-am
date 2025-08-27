# Sample businesses data
businesses_data = [
    {
        "name": "Tech Solutions Inc",
        "description": "Software development and IT consulting services",
        "financialMetrics": {
            "revenue": 1250000,
            "grossProfit": 875000,
            "netProfit": 625000,
            "totalCosts": 625000,
            "percentageChangeRevenue": 15.5,
            "percentageChangeGrossProfit": 12.8,
            "percentageChangeNetProfit": 18.2,
            "percentageChangeTotalCosts": -8.5
        },
        "metrics": {
            "documentsDue": 5,
            "outstandingInvoices": 12500,
            "pendingApprovals": 3,
            "accountingYearEnd": "31/12/2024"
        }
    },
    {
        "name": "Green Energy Co",
        "description": "Renewable energy solutions and consulting",
        "financialMetrics": {
            "revenue": 890000,
            "grossProfit": 623000,
            "netProfit": 445000,
            "totalCosts": 445000,
            "percentageChangeRevenue": 22.1,
            "percentageChangeGrossProfit": 25.3,
            "percentageChangeNetProfit": 28.7,
            "percentageChangeTotalCosts": -12.4
        },
        "metrics": {
            "documentsDue": 3,
            "outstandingInvoices": 8900,
            "pendingApprovals": 1,
            "accountingYearEnd": "31/12/2024"
        }
    },
    {
        "name": "Global Logistics Ltd",
        "description": "International shipping and logistics services",
        "financialMetrics": {
            "revenue": 2100000,
            "grossProfit": 1470000,
            "netProfit": 1050000,
            "totalCosts": 1050000,
            "percentageChangeRevenue": 8.9,
            "percentageChangeGrossProfit": 7.2,
            "percentageChangeNetProfit": 9.8,
            "percentageChangeTotalCosts": 5.1
        },
        "metrics": {
            "documentsDue": 8,
            "outstandingInvoices": 45000,
            "pendingApprovals": 4,
            "accountingYearEnd": "31/12/2024"
        }
    },
    {
        "name": "Creative Design Studio",
        "description": "Graphic design and branding services",
        "financialMetrics": {
            "revenue": 450000,
            "grossProfit": 315000,
            "netProfit": 225000,
            "totalCosts": 225000,
            "percentageChangeRevenue": 18.7,
            "percentageChangeGrossProfit": 20.1,
            "percentageChangeNetProfit": 22.5,
            "percentageChangeTotalCosts": -10.2
        },
        "metrics": {
            "documentsDue": 2,
            "outstandingInvoices": 12000,
            "pendingApprovals": 2,
            "accountingYearEnd": "31/12/2024"
        }
    },
    {
        "name": "Healthcare Partners",
        "description": "Medical practice management and consulting",
        "financialMetrics": {
            "revenue": 1800000,
            "grossProfit": 1260000,
            "netProfit": 900000,
            "totalCosts": 900000,
            "percentageChangeRevenue": 12.3,
            "percentageChangeGrossProfit": 11.8,
            "percentageChangeNetProfit": 13.5,
            "percentageChangeTotalCosts": 2.8
        },
        "metrics": {
            "documentsDue": 6,
            "outstandingInvoices": 28000,
            "pendingApprovals": 3,
            "accountingYearEnd": "31/12/2024"
        }
    },
    {
        "name": "Financial Advisory Group",
        "description": "Investment and financial planning services",
        "financialMetrics": {
            "revenue": 3200000,
            "grossProfit": 2240000,
            "netProfit": 1600000,
            "totalCosts": 1600000,
            "percentageChangeRevenue": 14.2,
            "percentageChangeGrossProfit": 16.8,
            "percentageChangeNetProfit": 19.5,
            "percentageChangeTotalCosts": -5.2
        },
        "metrics": {
            "documentsDue": 4,
            "outstandingInvoices": 35000,
            "pendingApprovals": 2,
            "accountingYearEnd": "31/12/2024"
        }
    },
    {
        "name": "Manufacturing Solutions",
        "description": "Industrial manufacturing and automation",
        "financialMetrics": {
            "revenue": 4500000,
            "grossProfit": 3150000,
            "netProfit": 2250000,
            "totalCosts": 2250000,
            "percentageChangeRevenue": 11.8,
            "percentageChangeGrossProfit": 13.2,
            "percentageChangeNetProfit": 15.7,
            "percentageChangeTotalCosts": 3.4
        },
        "metrics": {
            "documentsDue": 7,
            "outstandingInvoices": 68000,
            "pendingApprovals": 5,
            "accountingYearEnd": "31/12/2024"
        }
    },
    {
        "name": "Retail Innovations",
        "description": "E-commerce and retail technology solutions",
        "financialMetrics": {
            "revenue": 2800000,
            "grossProfit": 1960000,
            "netProfit": 1400000,
            "totalCosts": 1400000,
            "percentageChangeRevenue": 25.6,
            "percentageChangeGrossProfit": 28.9,
            "percentageChangeNetProfit": 32.1,
            "percentageChangeTotalCosts": -15.8
        },
        "metrics": {
            "documentsDue": 3,
            "outstandingInvoices": 42000,
            "pendingApprovals": 1,
            "accountingYearEnd": "31/12/2024"
        }
    },
    {
        "name": "Construction Dynamics",
        "description": "Commercial construction and project management",
        "financialMetrics": {
            "revenue": 3800000,
            "grossProfit": 2660000,
            "netProfit": 1900000,
            "totalCosts": 1900000,
            "percentageChangeRevenue": 9.4,
            "percentageChangeGrossProfit": 8.7,
            "percentageChangeNetProfit": 11.2,
            "percentageChangeTotalCosts": 4.1
        },
        "metrics": {
            "documentsDue": 9,
            "outstandingInvoices": 75000,
            "pendingApprovals": 6,
            "accountingYearEnd": "31/12/2024"
        }
    },
    {
        "name": "Legal Services Corp",
        "description": "Corporate law and legal consulting",
        "financialMetrics": {
            "revenue": 2200000,
            "grossProfit": 1540000,
            "netProfit": 1100000,
            "totalCosts": 1100000,
            "percentageChangeRevenue": 16.8,
            "percentageChangeGrossProfit": 18.2,
            "percentageChangeNetProfit": 21.5,
            "percentageChangeTotalCosts": -7.8
        },
        "metrics": {
            "documentsDue": 4,
            "outstandingInvoices": 28000,
            "pendingApprovals": 2,
            "accountingYearEnd": "31/12/2024"
        }
    },
    {
        "name": "Marketing Masters",
        "description": "Digital marketing and brand strategy",
        "financialMetrics": {
            "revenue": 950000,
            "grossProfit": 665000,
            "netProfit": 475000,
            "totalCosts": 475000,
            "percentageChangeRevenue": 19.3,
            "percentageChangeGrossProfit": 22.1,
            "percentageChangeNetProfit": 25.8,
            "percentageChangeTotalCosts": -11.5
        },
        "metrics": {
            "documentsDue": 2,
            "outstandingInvoices": 15000,
            "pendingApprovals": 1,
            "accountingYearEnd": "31/12/2024"
        }
    },
    {
        "name": "Real Estate Partners",
        "description": "Commercial real estate investment and management",
        "financialMetrics": {
            "revenue": 5200000,
            "grossProfit": 3640000,
            "netProfit": 2600000,
            "totalCosts": 2600000,
            "percentageChangeRevenue": 13.7,
            "percentageChangeGrossProfit": 15.2,
            "percentageChangeNetProfit": 17.8,
            "percentageChangeTotalCosts": 2.9
        },
        "metrics": {
            "documentsDue": 5,
            "outstandingInvoices": 89000,
            "pendingApprovals": 3,
            "accountingYearEnd": "31/12/2024"
        }
    },
    {
        "name": "Education Solutions",
        "description": "Online learning platforms and educational technology",
        "financialMetrics": {
            "revenue": 1600000,
            "grossProfit": 1120000,
            "netProfit": 800000,
            "totalCosts": 800000,
            "percentageChangeRevenue": 28.9,
            "percentageChangeGrossProfit": 31.5,
            "percentageChangeNetProfit": 35.2,
            "percentageChangeTotalCosts": -18.7
        },
        "metrics": {
            "documentsDue": 3,
            "outstandingInvoices": 22000,
            "pendingApprovals": 2,
            "accountingYearEnd": "31/12/2024"
        }
    },
    {
        "name": "Pharmaceutical Research",
        "description": "Drug development and clinical research",
        "financialMetrics": {
            "revenue": 8500000,
            "grossProfit": 5950000,
            "netProfit": 4250000,
            "totalCosts": 4250000,
            "percentageChangeRevenue": 7.8,
            "percentageChangeGrossProfit": 6.9,
            "percentageChangeNetProfit": 9.2,
            "percentageChangeTotalCosts": 5.8
        },
        "metrics": {
            "documentsDue": 6,
            "outstandingInvoices": 125000,
            "pendingApprovals": 4,
            "accountingYearEnd": "31/12/2024"
        }
    },
    {
        "name": "Transportation Systems",
        "description": "Public transportation and mobility solutions",
        "financialMetrics": {
            "revenue": 3100000,
            "grossProfit": 2170000,
            "netProfit": 1550000,
            "totalCosts": 1550000,
            "percentageChangeRevenue": 10.5,
            "percentageChangeGrossProfit": 11.8,
            "percentageChangeNetProfit": 13.4,
            "percentageChangeTotalCosts": 3.2
        },
        "metrics": {
            "documentsDue": 8,
            "outstandingInvoices": 55000,
            "pendingApprovals": 5,
            "accountingYearEnd": "31/12/2024"
        }
    },
    {
        "name": "Food & Beverage Co",
        "description": "Restaurant chain and food service management",
        "financialMetrics": {
            "revenue": 2800000,
            "grossProfit": 1960000,
            "netProfit": 1400000,
            "totalCosts": 1400000,
            "percentageChangeRevenue": 18.2,
            "percentageChangeGrossProfit": 20.5,
            "percentageChangeNetProfit": 23.8,
            "percentageChangeTotalCosts": -9.6
        },
        "metrics": {
            "documentsDue": 4,
            "outstandingInvoices": 38000,
            "pendingApprovals": 2,
            "accountingYearEnd": "31/12/2024"
        }
    },
    {
        "name": "Entertainment Media",
        "description": "Content creation and media production",
        "financialMetrics": {
            "revenue": 1900000,
            "grossProfit": 1330000,
            "netProfit": 950000,
            "totalCosts": 950000,
            "percentageChangeRevenue": 21.4,
            "percentageChangeGrossProfit": 24.7,
            "percentageChangeNetProfit": 27.9,
            "percentageChangeTotalCosts": -13.2
        },
        "metrics": {
            "documentsDue": 3,
            "outstandingInvoices": 25000,
            "pendingApprovals": 2,
            "accountingYearEnd": "31/12/2024"
        }
    },
    {
        "name": "Environmental Services",
        "description": "Waste management and environmental consulting",
        "financialMetrics": {
            "revenue": 1400000,
            "grossProfit": 980000,
            "netProfit": 700000,
            "totalCosts": 700000,
            "percentageChangeRevenue": 15.8,
            "percentageChangeGrossProfit": 17.2,
            "percentageChangeNetProfit": 19.5,
            "percentageChangeTotalCosts": -6.8
        },
        "metrics": {
            "documentsDue": 5,
            "outstandingInvoices": 18000,
            "pendingApprovals": 3,
            "accountingYearEnd": "31/12/2024"
        }
    },
    {
        "name": "Technology Consulting",
        "description": "IT strategy and digital transformation",
        "financialMetrics": {
            "revenue": 3600000,
            "grossProfit": 2520000,
            "netProfit": 1800000,
            "totalCosts": 1800000,
            "percentageChangeRevenue": 17.6,
            "percentageChangeGrossProfit": 19.8,
            "percentageChangeNetProfit": 22.4,
            "percentageChangeTotalCosts": -8.9
        },
        "metrics": {
            "documentsDue": 6,
            "outstandingInvoices": 48000,
            "pendingApprovals": 4,
            "accountingYearEnd": "31/12/2024"
        }
    },
    {
        "name": "Healthcare Technology",
        "description": "Medical devices and health IT solutions",
        "financialMetrics": {
            "revenue": 4200000,
            "grossProfit": 2940000,
            "netProfit": 2100000,
            "totalCosts": 2100000,
            "percentageChangeRevenue": 12.9,
            "percentageChangeGrossProfit": 14.3,
            "percentageChangeNetProfit": 16.7,
            "percentageChangeTotalCosts": 4.2
        },
        "metrics": {
            "documentsDue": 7,
            "outstandingInvoices": 72000,
            "pendingApprovals": 5,
            "accountingYearEnd": "31/12/2024"
        }
    },
    {
        "name": "Financial Services",
        "description": "Banking and financial technology solutions",
        "financialMetrics": {
            "revenue": 6800000,
            "grossProfit": 4760000,
            "netProfit": 3400000,
            "totalCosts": 3400000,
            "percentageChangeRevenue": 11.2,
            "percentageChangeGrossProfit": 12.8,
            "percentageChangeNetProfit": 14.9,
            "percentageChangeTotalCosts": 3.7
        },
        "metrics": {
            "documentsDue": 8,
            "outstandingInvoices": 95000,
            "pendingApprovals": 6,
            "accountingYearEnd": "31/12/2024"
        }
    },
    {
        "name": "Manufacturing Excellence",
        "description": "Advanced manufacturing and quality control",
        "financialMetrics": {
            "revenue": 3900000,
            "grossProfit": 2730000,
            "netProfit": 1950000,
            "totalCosts": 1950000,
            "percentageChangeRevenue": 13.4,
            "percentageChangeGrossProfit": 15.1,
            "percentageChangeNetProfit": 17.8,
            "percentageChangeTotalCosts": 2.5
        },
        "metrics": {
            "documentsDue": 6,
            "outstandingInvoices": 58000,
            "pendingApprovals": 4,
            "accountingYearEnd": "31/12/2024"
        }
    },
    {
        "name": "Retail Solutions",
        "description": "Point of sale and inventory management systems",
        "financialMetrics": {
            "revenue": 2400000,
            "grossProfit": 1680000,
            "netProfit": 1200000,
            "totalCosts": 1200000,
            "percentageChangeRevenue": 20.8,
            "percentageChangeGrossProfit": 23.5,
            "percentageChangeNetProfit": 26.9,
            "percentageChangeTotalCosts": -12.1
        },
        "metrics": {
            "documentsDue": 4,
            "outstandingInvoices": 32000,
            "pendingApprovals": 2,
            "accountingYearEnd": "31/12/2024"
        }
    },
    {
        "name": "Construction Management",
        "description": "Project planning and construction oversight",
        "financialMetrics": {
            "revenue": 2900000,
            "grossProfit": 2030000,
            "netProfit": 1450000,
            "totalCosts": 1450000,
            "percentageChangeRevenue": 16.2,
            "percentageChangeGrossProfit": 18.7,
            "percentageChangeNetProfit": 21.3,
            "percentageChangeTotalCosts": -7.4
        },
        "metrics": {
            "documentsDue": 7,
            "outstandingInvoices": 42000,
            "pendingApprovals": 5,
            "accountingYearEnd": "31/12/2024"
        }
    },
    {
        "name": "Legal Consulting",
        "description": "Specialized legal services and compliance",
        "financialMetrics": {
            "revenue": 1800000,
            "grossProfit": 1260000,
            "netProfit": 900000,
            "totalCosts": 900000,
            "percentageChangeRevenue": 19.5,
            "percentageChangeGrossProfit": 21.8,
            "percentageChangeNetProfit": 24.6,
            "percentageChangeTotalCosts": -10.3
        },
        "metrics": {
            "documentsDue": 3,
            "outstandingInvoices": 25000,
            "pendingApprovals": 2,
            "accountingYearEnd": "31/12/2024"
        }
    },
    {
        "name": "Digital Marketing Agency",
        "description": "Online marketing and social media management",
        "financialMetrics": {
            "revenue": 1200000,
            "grossProfit": 840000,
            "netProfit": 600000,
            "totalCosts": 600000,
            "percentageChangeRevenue": 26.8,
            "percentageChangeGrossProfit": 29.2,
            "percentageChangeNetProfit": 32.1,
            "percentageChangeTotalCosts": -18.5
        },
        "metrics": {
            "documentsDue": 2,
            "outstandingInvoices": 18000,
            "pendingApprovals": 1,
            "accountingYearEnd": "31/12/2024"
        }
    }
]

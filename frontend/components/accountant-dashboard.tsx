import React from 'react';
import { Card, CardHeader, CardBody, CardFooter } from 'shadcn';

const businesses = [
    { name: 'Business A', indicator: 'Revenue: $10,000' },
    { name: 'Business B', indicator: 'Revenue: $15,000' },
    { name: 'Business C', indicator: 'Revenue: $8,000' },
];

const AccountantDashboard: React.FC = () => {
    return (
        <div className="grid grid-cols-3 gap-4">
            {businesses.map((business, index) => (
                <Card key={index} className="shadow-lg">
                    <CardHeader>
                        <h2 className="text-lg font-bold">{business.name}</h2>
                    </CardHeader>
                    <CardBody>
                        <p>{business.indicator}</p>
                    </CardBody>
                    <CardFooter>
                        <button className="btn btn-primary">View Details</button>
                    </CardFooter>
                </Card>
            ))}
        </div>
    );
};

export default AccountantDashboard;

export const singleFormFields = [
  {
    key: 'CreditScore',
    label: 'Credit Score',
    type: 'number',
    min: 300,
    max: 900,
    description:
      'CreditScore can affect churn: customers with a higher credit score are generally less likely to leave the bank.',
  },
  {
    key: 'Geography',
    label: 'Geography',
    type: 'select',
    options: ['France', 'Germany', 'Spain', 'India'],
    description: "A customer's country/region; geography can influence their likelihood to leave the bank.",
  },
  {
    key: 'Gender',
    label: 'Gender',
    type: 'select',
    options: ['Male', 'Female'],
    description:
      "Customer's gender; useful for exploring whether gender plays a role in churn behaviour at this bank.",
  },
  {
    key: 'Age',
    label: 'Age',
    type: 'number',
    min: 18,
    max: 100,
    description:
      'Customer age in years; older customers tend to be more stable and less likely to leave than younger ones.',
  },
  {
    key: 'Tenure',
    label: 'Tenure (Years)',
    type: 'number',
    min: 0,
    max: 20,
    description:
      'Number of years the customer has been with the bank; longer-tenure customers are usually more loyal.',
  },
  {
    key: 'Balance',
    label: 'Balance',
    type: 'number',
    min: 0,
    max: 1000000,
    description:
      'Current account balance; customers with higher balances are generally less likely to leave the bank.',
  },
  {
    key: 'NumOfProducts',
    label: 'Products',
    type: 'number',
    min: 1,
    max: 4,
    description: 'Number of bank products the customer uses (e.g., accounts, loans, cards).',
  },
  {
    key: 'HasCrCard',
    label: 'Credit Card',
    type: 'select',
    options: [
      { label: 'Yes', value: 1 },
      { label: 'No', value: 0 },
    ],
    description:
      'Whether the customer has a credit card with the bank; card holders are often less likely to leave.',
  },
  {
    key: 'IsActiveMember',
    label: 'Active Member',
    type: 'select',
    options: [
      { label: 'Yes', value: 1 },
      { label: 'No', value: 0 },
    ],
    description:
      'Indicates if the customer is actively using bank services; active customers are less likely to churn.',
  },
  {
    key: 'EstimatedSalary',
    label: 'Estimated Salary',
    type: 'number',
    min: 0,
    max: 1000000,
    description:
      "Model's estimate of the customer’s yearly salary; lower-salary segments can show higher churn risk.",
  },
];

export const singleFormDefaults = {
  CreditScore: 650,
  Geography: 'Germany',
  Gender: 'Female',
  Age: 42,
  Tenure: 5,
  Balance: 125000,
  NumOfProducts: 2,
  HasCrCard: 1,
  IsActiveMember: 1,
  EstimatedSalary: 90000,
};

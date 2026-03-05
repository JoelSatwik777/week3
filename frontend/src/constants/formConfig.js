export const singleFormFields = [
  { key: 'CreditScore', label: 'Credit Score', type: 'number', min: 300, max: 900 },
  {
    key: 'Geography',
    label: 'Geography',
    type: 'select',
    options: ['France', 'Germany', 'Spain', 'India'],
  },
  {
    key: 'Gender',
    label: 'Gender',
    type: 'select',
    options: ['Male', 'Female'],
  },
  { key: 'Age', label: 'Age', type: 'number', min: 18, max: 100 },
  { key: 'Tenure', label: 'Tenure (Years)', type: 'number', min: 0, max: 20 },
  { key: 'Balance', label: 'Balance', type: 'number', min: 0, max: 1000000 },
  { key: 'NumOfProducts', label: 'Products', type: 'number', min: 1, max: 4 },
  {
    key: 'HasCrCard',
    label: 'Credit Card',
    type: 'select',
    options: [
      { label: 'Yes', value: 1 },
      { label: 'No', value: 0 },
    ],
  },
  {
    key: 'IsActiveMember',
    label: 'Active Member',
    type: 'select',
    options: [
      { label: 'Yes', value: 1 },
      { label: 'No', value: 0 },
    ],
  },
  { key: 'EstimatedSalary', label: 'Estimated Salary', type: 'number', min: 0, max: 1000000 },
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

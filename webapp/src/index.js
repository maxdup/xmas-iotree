import './index.scss';

console.log('IOT-seed');

fetch('http://localhost:5000/api/switch').then((response) => {
  response.json().then((body) => {
    console.log('body', body);
  });
});



import './index.scss';

console.log('IOT-seed');


let example_getConfig = () => {
  fetch('http://localhost:5000/api/config/', {
    method: 'GET',
    headers: { 'Content-Type': 'application/json;charset=UTF-8',
               'Accept': 'application/json, text/plain',
               'Access-Control-Allow-Origin': '*'}
  }).then((response) => {
    response.json().then((body) => {
      console.log('response', body);
    });
  });
}
example_getConfig();

let example_setConfig = () => {

  let nleds = 3;
  let positions = [];

  for (let i = 0; i < nleds; i++){
    positions.push({
      x: Math.floor(Math.random() * 2 -1),
      y: Math.floor(Math.random() * 2 -1),
      z: Math.floor(Math.random() * 2 -1)
    });
  }

  let reqbody = JSON.stringify({
  positions: positions
  });

  fetch('http://localhost:5000/api/config/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json;charset=UTF-8',
               'Accept': 'application/json, text/plain',
               'Access-Control-Allow-Origin': '*'},
    body: reqbody
  }).then((response) => {
    response.json().then((body) => {
      console.log('response', body);
    });
  });
}

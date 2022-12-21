import './index.scss';

console.log('IOT-seed');

const NLED = 400;

let example_getConfig = () => {
  fetch(window.conf.deviceUrl + '/api/config/', {
    method: 'GET',
  }).then((response) => {
    response.json().then((body) => {
      console.log('response', body);
    });
  });
}

let example_setConfig = () => {

  let positions = [];

  for (let i = 0; i < NLED; i++){
    positions.push({
      x: Math.floor(Math.random() * 2 -1),
      y: Math.floor(Math.random() * 2 -1),
      z: Math.floor(Math.random() * 2 -1)
    });
  }

  let reqbody = JSON.stringify({
    positions: positions
  });

  fetch(window.conf.deviceUrl + '/api/config/', {
    method: 'POST',
    body: reqbody,
    headers: { 'Content-Type': 'application/json' }
  }).then((response) => {
    response.json().then((body) => {
      console.log('response', body);
    });
  });
}


let offset = 0;

let example_postLeds = () => {
  offset += 0.4;
  let colors = [];
  for (let i = 0; i < NLED; i++){
    let y = Math.sin((i+offset) * 0.20);
    let b = (y + 1) / 2 * 255;
    colors.push({r:Math.min(b+50, 255), g: 0, b: b})
  }

  let reqbody = JSON.stringify({
    colors: colors
  });
  fetch(window.conf.deviceUrl + '/api/leds/', {
    method: 'POST',
    body: reqbody,
    headers: { 'Content-Type': 'application/json' }
  });

  setTimeout(example_postLeds, 100);
}


example_postLeds();


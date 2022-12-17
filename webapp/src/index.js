import './index.scss';

console.log('IOT-seed');


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

let example_postLeds = () => {
  let colors = [{ r:255, g:255, b:0, },
                { r:0, g:255, b:255, },
                { r:255, g:0, b:255, }];

  let reqbody = JSON.stringify({
    colors: colors
  });
  fetch(window.conf.deviceUrl + '/api/leds/', {
    method: 'POST',
    body: reqbody,
    headers: { 'Content-Type': 'application/json' }
  }).then((response) => {
    response.json().then((body) => {
      console.log('response', body);
    });
  });
}

example_postLeds();

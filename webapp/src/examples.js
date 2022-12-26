import './index.scss';

console.log('IOT-seed');

const NLED = 400;

let example_getConfig = () => {
  // Get the current led configuration
  fetch(window.conf.deviceUrl + '/api/config/', {
    method: 'GET',
  }).then((response) => {
    response.json().then((body) => {
      console.log('response', body);
    });
  });
}

let example_setConfig = () => {
  // Set the current led configuration
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
  // post a led configuration
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

let myscript_name = 'myscript.py'

let example_post_script = () => {
  // save and run a given script
  let content = "print('hello world')\nprint('¯\_(ツ)_/¯ ლ(ಠ益ಠლ) (;´༎ ຶД༎ ຶ`) éèê')";
  let reqbody = content
  fetch(window.conf.deviceUrl + '/api/script/' + myscript_name, {
    method: 'POST',
    body: reqbody,
    headers: { 'Content-Type': 'text/plain;charset=UTF-8' }
  }).then((resp) => {
    console.log('ok', resp);
  });
}

let example_get_script = () => {
  // get a given script
  fetch(window.conf.deviceUrl + '/api/script/' + myscript_name, {
    method: 'GET',
  }).then((resp) => {
    console.log('ok', resp);
  });
}

let example_put_script = () => {
  // runs a given script
  fetch(window.conf.deviceUrl + '/api/script/' + myscript_name, {
    method: 'PUT',
  }).then((resp) => {
    console.log('ok', resp);
  });
}

let example_get_scripts = () => {
  // get the list of scripts
  fetch(window.conf.deviceUrl + '/api/script/', {
    method: 'GET',
  }).then((resp) => {
    console.log('ok', resp);
  });
}

example_put_script();


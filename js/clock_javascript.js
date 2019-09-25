let size = 25;
let columns = Array.from(document.getElementsByClassName('column'));
let d, c;
let classList = ['visible', 'close', 'far', 'far', 'distant', 'distant'];
let use24HourClock = false;

function padClock(p, n) {
  return p + ('0' + n).slice(-2);
}

function getClock() {
  d = new Date();
  var ampm = d.getHours >= 12 ? 'PM' : 'AM';
  return [
  use24HourClock ? d.getHours() : d.getHours() % 12 || 12,
  d.getMinutes(),
  d.getSeconds(),
  ampm].

  reduce(padClock, '');
}

function getClass(n, i2) {
  return classList.find((class_, classIndex) => Math.abs(n - i2) === classIndex) || '';
}

let loop = setInterval(() => {
  c = getClock();
  var pm_am = document.getElementsByClassName("pm_or_am");
  console.log(pm_am);
  pm_am[0].style.content = c[6];
  console.log(pm_am[0].style.content);
  columns.forEach((ele, i) => {
    let n = +c[i];
    let offset = -n * size;
    ele.style.transform = `translateY(calc(10vh + ${offset}px - ${size / 2}px))`;
    Array.from(ele.children).forEach((ele2, i2) => {
      ele2.className = 'num ' + getClass(n, i2);
    });
  });
}, 200 + Math.E * 10);
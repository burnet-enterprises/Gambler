'use strict';
(function() {
  function drawPills() {
    //value is the number of red pills
    //two random sorts: one to shuffle the kinds, another to shuffle the stacking
    const slider = document.getElementById('pillx')
    const bottleSize = parseInt(slider.max, 10)
    const value      = parseInt(slider.value) //The number of red pills
    let pills = []
    switch (bottleSize) {
      case 100:
      for (let i=0; i<10; i++) {
        for (let j=0; j<10; j++) {
          const dx=Math.random()+Math.random()
          const dy=Math.random()+Math.random()+Math.random()
          if (i==0) {
            if (j<2) {
              pills.push({x: 22*(j+3)-22+dx, y:12+dy, sort: Math.random()})
            }
            else if (j>7) {
              pills.push({x: 22*(j-3)-22+dx, y:12+dy, sort: Math.random()})
            }
            else {
              pills.push({x: 22*j-22+dx, y:32+dy, sort: Math.random()})
            }
          }
          else {
            pills.push({x: 18*j-5+dx, y:30+26*i+dy, sort: Math.random()})
          }
        }
      }
      break

      case 1000:
      for (let i=0; i<50; i++) {
        for (let j=0; j<20; j++) {
          const dx=Math.random()+Math.random()+Math.random()+Math.random()+Math.random()
          const dy=(Math.random()+Math.random()+Math.random())/2
          if (i==49 && j<3) {
            pills.push({x: 9*(j+7)+dx, y:36+dy, sort: Math.random()})
          }
          else if (i==49 && j>16) {
            pills.push({x: 9*(j-7)+dx, y:36+dy, sort: Math.random()})
          }
          else if (i==48 && j<2) {
            pills.push({x: 9*(j+5)+dx, y:36+dy, sort: Math.random()})
          }
          else if (i==48 && j>17) {
            pills.push({x: 9*(j-5)+dx, y:36+dy, sort: Math.random()})
          }
          else if (i==47 && j==0) {
            pills.push({x: 36+dx, y:36+dy, sort: Math.random()})
          }
          else if (i==47 && j==19) {
            pills.push({x: 135+dx, y:36+dy, sort: Math.random()})
          }
          else if (i<5 && j==0) {
            pills.push({x: 9*(i+5)+dx, y:30+dy, sort: Math.random()})
          }
          else if (i<5 && j==19) {
            pills.push({x: 9*(i+10)+dx, y:30+dy, sort: Math.random()})
          }
          else if (i==0 && j==1) {
            pills.push({x: 36+dx, y:30+dy, sort: Math.random()})
          }
          else if (i==0 && j==18) {
            pills.push({x: 135+dx, y:30+dy, sort: Math.random()})
          }
          else if (i==1 && j==1) {
            pills.push({x: 27+dx, y:36+dy, sort: Math.random()})
          }
          else if (i==1 && j==18) {
            pills.push({x: 144+dx, y:36+dy, sort: Math.random()})
          }
          else {
            pills.push({x: 9*j+dx, y:42+5*i+dy, sort: Math.random()})
          }
        }
      }
      break

      default:
      return false
    }

    let i=0
    pills.sort((a, b)=>{return a.sort-b.sort})
    for (let pill of pills) {
      pill.sort = Math.random()
      pill.kind = i++ < value
    }

    const svg = document.getElementById('pills')
    while (svg.hasChildNodes()) {
      svg.removeChild(svg.firstChild)
    }
    for (const pill of pills.sort((a, b)=>{return a.sort-b.sort})) {
      const p = document.createElementNS('http://www.w3.org/2000/svg', 'use')
      p.setAttributeNS('http://www.w3.org/1999/xlink', 'href', pill.kind ? '#red-pill' : '#blue-pill')
      p.setAttribute('x', '0')
      p.setAttribute('y', '0')
      p.setAttribute('transform', [
        `translate(${pill.x},${pill.y})`,
        bottleSize == 1000 ? 'scale(0.15)' : 'scale(0.5)',
        `rotate(${360*Math.random()} 30,30)`
      ].join(' '))
      svg.appendChild(p)
    }
  }

  function setPillCount(n) {
    const slider = document.getElementById('pillx')
    const currentMax = slider.max
    const currentVal = slider.value
    slider.max   = n
    slider.value = Math.round(parseInt(n, 10) * parseInt(currentVal, 10) / parseInt(currentMax, 10))
    drawPills()
  }

  window.addEventListener('load', () => {
    document.getElementById('pillx').addEventListener('change', drawPills)
    document.getElementById('shaker').addEventListener('click', drawPills)
    document.getElementById('pill-bottle').addEventListener('click', drawPills)

    for (const input of document.getElementsByTagName('input')) {
      if (input.type == 'hidden' && input.name == 'pill-count') {
        input.addEventListener('change', e=>{
          setPillCount(e.target.value)
        })
      }
    }
    drawPills()
  })
})()


(() => {
  const svgEl = document.getElementById('globe');
  if (!svgEl) return;
  if (typeof d3 === 'undefined' || typeof topojson === 'undefined') return;

  const dataEl = document.getElementById('globePointsData');
  let points = [];
  try {
    points = JSON.parse(dataEl.textContent || '[]');
  } catch (e) {
    points = [];
  }

  const WORLD_URL = 'https://cdn.jsdelivr.net/npm/world-atlas@2.0.2/countries-110m.json';

  const stage = svgEl.parentElement;
  const tooltip = document.getElementById('globeTooltip');
  const listEl = document.getElementById('globeList');

  const state = {
    width: 600,
    height: 600,
    rotation: [-20, -20, 0],
    isDragging: false,
    autoRotate: true,
    selectedId: null,
  };

  const svg = d3.select(svgEl);
  const projection = d3.geoOrthographic().precision(0.6);
  const path = d3.geoPath(projection);

  const defs = svg.append('defs');
  const oceanGrad = defs.append('radialGradient')
    .attr('id', 'oceanGradient')
    .attr('cx', '50%').attr('cy', '45%').attr('r', '55%');
  oceanGrad.append('stop').attr('offset', '0%').attr('stop-color', '#f7f6f4');
  oceanGrad.append('stop').attr('offset', '65%').attr('stop-color', '#efefed');
  oceanGrad.append('stop').attr('offset', '100%').attr('stop-color', '#dad9d4');

  const glow = defs.append('radialGradient')
    .attr('id', 'globeGlow')
    .attr('cx', '50%').attr('cy', '50%').attr('r', '55%');
  glow.append('stop').attr('offset', '75%').attr('stop-color', 'rgba(17,17,16,0)');
  glow.append('stop').attr('offset', '100%').attr('stop-color', 'rgba(17,17,16,0.18)');

  const gGlow    = svg.append('g');
  const gOcean   = svg.append('g');
  const gGraticule = svg.append('g');
  const gLand    = svg.append('g');
  const gArcs    = svg.append('g');
  const gPoints  = svg.append('g');

  const glowCircle = gGlow.append('circle').attr('fill', 'url(#globeGlow)');
  const oceanCircle = gOcean.append('circle').attr('fill', 'url(#oceanGradient)').attr('stroke', '#cfcecb').attr('stroke-width', 1);

  const graticule = d3.geoGraticule10();
  const graticulePath = gGraticule.append('path')
    .datum(graticule)
    .attr('fill', 'none')
    .attr('stroke', 'rgba(17,17,16,0.08)')
    .attr('stroke-width', 0.6);

  let landPath = null;

  function setSize() {
    const rect = stage.getBoundingClientRect();
    const size = Math.min(rect.width, rect.height);
    state.width = rect.width;
    state.height = rect.height;
    svg.attr('viewBox', `0 0 ${state.width} ${state.height}`)
       .attr('width', state.width)
       .attr('height', state.height);

    const r = size / 2 - 10;
    projection
      .scale(r)
      .translate([state.width / 2, state.height / 2]);

    glowCircle
      .attr('cx', state.width / 2)
      .attr('cy', state.height / 2)
      .attr('r', r + 20);
    oceanCircle
      .attr('cx', state.width / 2)
      .attr('cy', state.height / 2)
      .attr('r', r);

    render();
  }

  function render() {
    projection.rotate(state.rotation);
    graticulePath.attr('d', path);
    if (landPath) landPath.attr('d', path);
    renderPoints();
  }

  function isVisible(lng, lat) {
    const rot = projection.rotate();
    const lambda = -rot[0] * Math.PI / 180;
    const phi = -rot[1] * Math.PI / 180;
    const l = lng * Math.PI / 180;
    const p = lat * Math.PI / 180;
    const cosC = Math.sin(phi) * Math.sin(p) + Math.cos(phi) * Math.cos(p) * Math.cos(l - lambda);
    return cosC >= -0.02;
  }

  function renderPoints() {
    const sel = gPoints.selectAll('g.globe-pin').data(points, d => d.id);

    const enter = sel.enter().append('g')
      .attr('class', 'globe-pin')
      .style('cursor', 'pointer')
      .on('mouseenter', function (event, d) {
        d3.select(this).classed('is-hover', true);
        showTooltip(event, d);
      })
      .on('mousemove', function (event) {
        moveTooltip(event);
      })
      .on('mouseleave', function () {
        d3.select(this).classed('is-hover', false);
        hideTooltip();
      })
      .on('click', function (event, d) {
        event.stopPropagation();
        goToPoint(d);
      });

    enter.append('circle').attr('class', 'pin-pulse').attr('r', 8);
    enter.append('circle').attr('class', 'pin-ring-outer').attr('r', 11);
    enter.append('circle').attr('class', 'pin-ring').attr('r', 8);
    enter.append('circle').attr('class', 'pin-core').attr('r', 5);
    enter.append('circle').attr('class', 'pin-inner').attr('r', 1.8);

    const merged = enter.merge(sel);
    merged.each(function (d) {
      const visible = isVisible(d.lng, d.lat);
      const coords = projection([d.lng, d.lat]);
      const g = d3.select(this);
      if (!visible || !coords) {
        g.style('display', 'none');
        return;
      }
      g.style('display', null)
        .attr('transform', `translate(${coords[0]}, ${coords[1]})`)
        .classed('is-selected', state.selectedId === d.id);
    });

    sel.exit().remove();
  }

  function showTooltip(event, d) {
    if (!tooltip) return;
    tooltip.querySelector('.globe-tooltip-loc').textContent = d.location;
    tooltip.querySelector('.globe-tooltip-title').textContent = d.title;
    tooltip.classList.add('is-visible');
    tooltip.setAttribute('aria-hidden', 'false');
    moveTooltip(event);
  }
  function moveTooltip(event) {
    if (!tooltip) return;
    const rect = stage.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    tooltip.style.transform = `translate(${x + 16}px, ${y - 20}px)`;
  }
  function hideTooltip() {
    if (!tooltip) return;
    tooltip.classList.remove('is-visible');
    tooltip.setAttribute('aria-hidden', 'true');
  }

  function goToPoint(d) {
    state.selectedId = d.id;
    const target = [-d.lng, -d.lat, 0];
    state.autoRotate = false;
    const start = state.rotation.slice();
    d3.transition().duration(900).ease(d3.easeCubicInOut).tween('rot', () => {
      const interp = d3.interpolate(start, target);
      return (t) => {
        state.rotation = interp(t);
        render();
      };
    }).on('end', () => {
      setTimeout(() => {
        window.location.href = `/post/${d.id}`;
      }, 320);
    });
  }

  function rotateTo(d, { navigate = false } = {}) {
    state.selectedId = d.id;
    const target = [-d.lng, -d.lat, 0];
    state.autoRotate = false;
    const start = state.rotation.slice();
    d3.transition().duration(900).ease(d3.easeCubicInOut).tween('rot', () => {
      const interp = d3.interpolate(start, target);
      return (t) => {
        state.rotation = interp(t);
        render();
      };
    }).on('end', () => {
      if (navigate) window.location.href = `/post/${d.id}`;
    });
  }

  const drag = d3.drag()
    .on('start', () => {
      state.isDragging = true;
      state.autoRotate = false;
      svgEl.classList.add('is-dragging');
    })
    .on('drag', (event) => {
      const k = 0.35;
      const [x, y, z] = state.rotation;
      state.rotation = [
        x + event.dx * k,
        Math.max(-80, Math.min(80, y - event.dy * k)),
        z,
      ];
      render();
    })
    .on('end', () => {
      state.isDragging = false;
      svgEl.classList.remove('is-dragging');
    });

  svg.call(drag);

  let lastTs = performance.now();
  function tick(ts) {
    const dt = ts - lastTs;
    lastTs = ts;
    if (state.autoRotate && !state.isDragging) {
      state.rotation = [state.rotation[0] + dt * 0.006, state.rotation[1], state.rotation[2]];
      render();
    }
    requestAnimationFrame(tick);
  }

  let resumeTimer = null;
  function scheduleAutoRotateResume() {
    clearTimeout(resumeTimer);
    resumeTimer = setTimeout(() => { state.autoRotate = true; }, 5000);
  }
  stage.addEventListener('mouseleave', scheduleAutoRotateResume);
  svgEl.addEventListener('pointerup', scheduleAutoRotateResume);

  if (listEl) {
    listEl.querySelectorAll('.globe-list-item').forEach(btn => {
      btn.addEventListener('mouseenter', () => {
        const id = parseInt(btn.dataset.id, 10);
        const d = points.find(p => p.id === id);
        if (!d) return;
        state.selectedId = d.id;
        state.autoRotate = false;
        renderPoints();
      });
      btn.addEventListener('mouseleave', () => {
        scheduleAutoRotateResume();
      });
      btn.addEventListener('click', () => {
        const id = parseInt(btn.dataset.id, 10);
        const d = points.find(p => p.id === id);
        if (!d) return;
        rotateTo(d, { navigate: true });
      });
    });
  }

  d3.json(WORLD_URL).then((world) => {
    const land = topojson.feature(world, world.objects.countries);
    landPath = gLand.append('path')
      .datum(land)
      .attr('fill', '#111110')
      .attr('stroke', '#2a2a28')
      .attr('stroke-width', 0.4);
    render();
  }).catch(() => {
    gLand.append('text')
      .attr('x', state.width / 2)
      .attr('y', state.height / 2)
      .attr('text-anchor', 'middle')
      .attr('fill', '#999994')
      .attr('font-size', 12)
      .text('Harita yüklenemedi.');
  });

  window.addEventListener('resize', setSize);
  setSize();
  requestAnimationFrame(tick);
})();

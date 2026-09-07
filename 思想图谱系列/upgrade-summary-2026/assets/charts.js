(function () {
  var style = getComputedStyle(document.documentElement);
  var accent = style.getPropertyValue('--accent').trim();
  var accent2 = style.getPropertyValue('--accent2').trim();
  var ink = style.getPropertyValue('--ink').trim();
  var muted = style.getPropertyValue('--muted').trim();
  var rule = style.getPropertyValue('--rule').trim();
  var bg2 = style.getPropertyValue('--bg2').trim();

  var volumes = ['物理学', '天文学', '化学', '医学', '宗教学', '语言学', '计算机科学'];

  // --- 图 2：汉字数前后对比 ---
  var el1 = document.getElementById('chart-chars');
  if (el1) {
    var chart1 = echarts.init(el1, null, { renderer: 'svg' });
    chart1.setOption({
      color: [bg2, accent],
      tooltip: { trigger: 'axis', appendToBody: true },
      legend: { data: ['升级前', '升级后'], textStyle: { color: ink } },
      grid: { left: 60, right: 20, top: 40, bottom: 40 },
      xAxis: {
        type: 'category', data: volumes,
        axisLine: { lineStyle: { color: rule } },
        axisLabel: { color: ink, interval: 0, rotate: 28 }
      },
      yAxis: {
        type: 'value', name: '汉字数',
        axisLine: { lineStyle: { color: rule } },
        axisLabel: { color: muted },
        splitLine: { lineStyle: { color: rule } }
      },
      series: [
        {
          name: '升级前', type: 'bar', barMaxWidth: 22,
          data: [4936, 2438, 1916, 1637, 1792, 1625, 1821],
          itemStyle: { color: muted, opacity: 0.55 }
        },
        {
          name: '升级后', type: 'bar', barMaxWidth: 22,
          data: [14408, 13535, 10946, 11152, 13771, 12713, 14935],
          itemStyle: { color: accent },
          label: { show: true, position: 'top', color: accent, fontWeight: 600, fontSize: 10, formatter: function (p) { return (p.value / 10000).toFixed(1) + '万'; } }
        }
      ],
      animation: false
    });
    window.addEventListener('resize', function () { chart1.resize(); });
  }

  // --- 图 3：思维导图(柱) + 解释块(线,右轴) ---
  var el2 = document.getElementById('chart-blocks');
  if (el2) {
    var chart2 = echarts.init(el2, null, { renderer: 'svg' });
    chart2.setOption({
      color: [accent2, accent],
      tooltip: { trigger: 'axis', appendToBody: true },
      legend: { data: ['思维导图', '解释块'], textStyle: { color: ink } },
      grid: { left: 60, right: 60, top: 40, bottom: 40 },
      xAxis: {
        type: 'category', data: volumes,
        axisLine: { lineStyle: { color: rule } },
        axisLabel: { color: ink, interval: 0, rotate: 28 }
      },
      yAxis: [
        {
          type: 'value', name: '思维导图（张）',
          axisLine: { lineStyle: { color: rule } },
          axisLabel: { color: muted },
          splitLine: { lineStyle: { color: rule } }
        },
        {
          type: 'value', name: '解释块（个）',
          axisLine: { lineStyle: { color: rule } },
          axisLabel: { color: muted },
          splitLine: { show: false }
        }
      ],
      series: [
        {
          name: '思维导图', type: 'bar', barMaxWidth: 26,
          data: [15, 16, 16, 14, 10, 11, 10],
          itemStyle: { color: accent2 }
        },
        {
          name: '解释块', type: 'line', yAxisIndex: 1, smooth: true, symbolSize: 8,
          data: [27, 33, 26, 24, 25, 26, 25],
          itemStyle: { color: accent },
          lineStyle: { width: 3 },
          label: { show: true, position: 'top', color: accent, fontWeight: 600 }
        }
      ],
      animation: false
    });
    window.addEventListener('resize', function () { chart2.resize(); });
  }
})();

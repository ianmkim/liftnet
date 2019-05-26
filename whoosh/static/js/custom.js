var lineData = [ 
  { "x": 1,   "y": 5},  
  { "x": 100,  "y": 5}, 
  { "x": 200, "y": 5}
];
var lineData2 = [ 
    { "x": 1,   "y": 5},  
    { "x": 100,  "y": 10}, 
    { "x": 200, "y": 5}
  ];
var lineData3 = [ 
    { "x": 1,   "y": 5},  
    { "x": 100,  "y": 0}, 
    { "x": 200, "y": 5}
  ];
var lineData4 = [ 
  { "x": 1,   "y": 7},  
  { "x": 100,  "y": 8}, 
  { "x": 200, "y": 7}
];

var lineFunction = d3.svg.line()
  .x(function(d) { return d.x; })
  .y(function(d) { return d.y; })
  .interpolate("monotone");
var svgContainer =d3.select("div.text-field").append("svg")
  .attr("class", 'border');
var lineGraph = svgContainer.append("path")
.attr("d", lineFunction(lineData))
.attr("class", 'line')
.attr("stroke-width", 1)
.attr("fill", "none");
$("input[type='text']").hover(function(){
  console.log($(this).parent().siblings('label'));
    d3.select(".line").transition()
            .duration(150).ease('sin')
      .attr("d", lineFunction(lineData2)).transition()
            .duration(150).ease('sin')
      .attr("d", lineFunction(lineData3)).transition()
            .duration(150).ease('sin')
      .attr("d", lineFunction(lineData));
},
function(){
  if( !$(this).val() ) {
      $(this).parent().siblings('label').removeClass('active');
  }else{
      $(this).parent().siblings('label').addClass('active');
  }
  d3.select(".line").transition()
            .duration(150).ease('sin')
      .attr("d", lineFunction(lineData4)).transition()
            .duration(150).ease('sin')
      .attr("d", lineFunction(lineData));
});
$("input[type='text']").focusin(function(){
  $(this).parent().siblings('label').addClass('focus');
});
$("input[type='text']").focusout(function(){
  $(this).parent().siblings('label').removeClass('focus');
  if( !$(this).val() ) {
      $(this).parent().siblings('label').removeClass('active');
  }else{
      $(this).parent().siblings('label').addClass('active');
  }
});


$("#inpt_search").on('focus', function () {
	$(this).parent('label').addClass('active');
});

$("#inpt_search").on('blur', function () {
	if($(this).val().length == 0)
		$(this).parent('label').removeClass('active');
});
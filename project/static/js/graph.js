function render(data){
  var node_color = '#38F'
  var node_mouse_color = "#4169e1"

  $("#graph").cytoscape({
        layout: {name: "concentric"} ,
        style: cytoscape.stylesheet()
            .selector('node')
              .css({
                  'background-color': node_color,
                  'content': 'data(id)',
                  'width': 'data(weight)',
                  'height': 'data(weight)', 
                  'text-valign': 'center', 
                  'text-halign': 'center',
                  'text-outline-width': 4,
                  'text-outline-color': node_color
              })
            .selector("edge")
              .css({
                  'width': "data(weight)"
              })
            .selector()
              .css({
              })
  })
  
  var cy = $("#graph").cytoscape("get")

  cy.add({
      group: "nodes",
      data: { id: data.center, weight: 100, center: true, url: data.word.url},
  })

  $.each(data.word.rel, function(i, item){
        cy.add([ { group: "nodes", data: { id: i, pre_weight:0, weight: item*80 + 30, center: false } }  
                    ,{ group: "edges", data: { id: "e"+i, source: data.center,  target: i, weight: 0.1} }
        ])
  })

  cy.nodes().on("click", function(){    
      if (this.data("center")){
          var url = "http://baike.baidu.com/search/word?word=" + this.id() + "&pic=1&sug=1&enc=utf-8"
          window.open(url)
      }else{
          cy.center(this)
          newword = this.id()
          submit_word(newword)
      }
  });

  cy.nodes().on("mouseover", function(){
    this.css("background", node_mouse_color).css("opacity", 0.7)
  })
  cy.nodes().on("mouseout", function(){
    this.css("background-color", node_color).css("opacity", 1)
  })

}
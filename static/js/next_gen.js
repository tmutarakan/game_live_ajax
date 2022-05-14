let refreshIntervalId = setInterval(function() {
           const request = new XMLHttpRequest();
           request.open('GET', `/next_gen`);
           request.onload = () => {
               const response = JSON.parse(request.responseText);
               document.getElementsByClassName("counter")[0].textContent = response['counter'];
               if (response['repeat'] === true) {
                   alert("Game Over");
                   clearInterval(refreshIntervalId);
               }
               for (let i=0; i<response['old_world'].length; i++) {
                   for (let j=0; j<response['old_world'][i].length; j++) {
                       if (response['world'][i][j]) {
                           document.getElementById(i+" "+j).setAttribute("class", "cell living-cell");
                       } else if (response['old_world'][i][j] && response['world'][i][j]===0) {
                           document.getElementById(i+" "+j).setAttribute("class", "cell dead-cell");
                       } else {
                           document.getElementById(i+" "+j).setAttribute("class", "cell");
                       }
                            }
                        }
                    };
                    request.send();
                    }, 1000);
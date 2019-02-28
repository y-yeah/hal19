let count = 0;
window.onload = () => {
  const capturePic = () => {
    const photo = document.getElementById("photo");
    // const button = document.getElementById("button");
    // button.addEventListener("click", () => {
    axios
      .get("/photo", {
        crossorigin: true,
        headers: {
          "Access-Control-ALlow-Origin": "*"
        }
      })
      .then(res => {
        console.log(res);
        axios
          .get("/photo/date", {
            crossorigin: true,
            headers: {
              "Access-Control-ALlow-Origin": "*"
            }
          })
          .then(nowRes => {
            console.log(nowRes);

            // const arrayBufferToBase64 = buffer => {
            //   let binary = "";
            //   let bytes = new Uint8Array(buffer);
            //   let len = bytes.byteLength;
            //   for (var i = 0; i < len; i++) {
            //     binary += String.fromCharCode(bytes[i]);
            //   }
            //   return window.btoa(binary);
            // };
            const arrayBufferToBase64 = arrayBuffer => {
              let base64 = "";
              const encodings =
                "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

              const bytes = new Uint8Array(arrayBuffer);
              const byteLength = bytes.byteLength;
              const byteRemainder = byteLength % 3;
              const mainLength = byteLength - byteRemainder;

              let a, b, c, d;
              let chunk;

              // Main loop deals with bytes in chunks of 3
              for (var i = 0; i < mainLength; i = i + 3) {
                // Combine the three bytes into a single integer
                chunk = (bytes[i] << 16) | (bytes[i + 1] << 8) | bytes[i + 2];

                // Use bitmasks to extract 6-bit segments from the triplet
                a = (chunk & 16515072) >> 18; // 16515072 = (2^6 - 1) << 18
                b = (chunk & 258048) >> 12; // 258048   = (2^6 - 1) << 12
                c = (chunk & 4032) >> 6; // 4032     = (2^6 - 1) << 6
                d = chunk & 63; // 63       = 2^6 - 1

                // Convert the raw binary segments to the appropriate ASCII encoding
                base64 +=
                  encodings[a] + encodings[b] + encodings[c] + encodings[d];
              }

              // Deal with the remaining bytes and padding
              if (byteRemainder === 1) {
                chunk = bytes[mainLength];

                a = (chunk & 252) >> 2; // 252 = (2^6 - 1) << 2

                // Set the 4 least significant bits to zero
                b = (chunk & 3) << 4; // 3   = 2^2 - 1

                base64 += encodings[a] + encodings[b] + "==";
              } else if (byteRemainder === 2) {
                chunk = (bytes[mainLength] << 8) | bytes[mainLength + 1];

                a = (chunk & 64512) >> 10; // 64512 = (2^6 - 1) << 10
                b = (chunk & 1008) >> 4; // 1008  = (2^6 - 1) << 4

                // Set the 2 least significant bits to zero
                c = (chunk & 15) << 2; // 15    = 2^4 - 1

                base64 += encodings[a] + encodings[b] + encodings[c] + "=";
              }

              return base64;
            };
            for (let i = count; i < res.data.length; i++) {
              const hvrbox = document.createElement("div");
              const hvrbox_layer_top = document.createElement("div");
              const hvrbox_text = document.createElement("a");
              hvrbox.className = "hvrbox";
              hvrbox.setAttribute(
                "style",
                `background-image: url("data:image/jpg;base64, ${arrayBufferToBase64(
                  res.data[i]
                )}")`
              );
              let nowString = "";
              nowRes.data[i].forEach(char => {
                if (char !== ",") {
                  nowString += char;
                }
              });
              hvrbox_layer_top.className = "hvrbox_layer_top";
              hvrbox_text.className = "hvrtxt";
              hvrbox_text.innerText = nowString;
              hvrbox_layer_top.appendChild(hvrbox_text);
              hvrbox.appendChild(hvrbox_layer_top);
              photo.appendChild(hvrbox);
              count++;
            }
            document.getElementById("dscr").innerText =
              res.data.length + " faces have been detected.";
          })
          .catch(err => {
            console.log(err);
          });
      })
      .catch(err => {
        console.log(err);
      });
  };
  setInterval(capturePic, 10);
};

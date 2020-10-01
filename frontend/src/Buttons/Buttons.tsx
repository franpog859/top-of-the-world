import React from "react";
import "./Buttons.css";
import Button from "react-bootstrap/Button";
import Ripples from "react-ripples";

interface ButtonsProps {
  clickMapButton: () => void;
  clickAboutButton: () => void;
  isMapButtonClicked: boolean;
}

function Buttons({
  clickMapButton,
  clickAboutButton,
  isMapButtonClicked
}: ButtonsProps) {
  const buttonStyle = {
    background: "#c7b198",
    color: "#f0ece3",
    borderRadius: "25px",
    textDecoration: "none",
    fontSize: "calc(10px + 2vmin)",
    margin: "5px"
  };

  return (
    <div className="Buttons" data-testid="Buttons">
      <header className="Buttons-header">
        <Ripples className="Buttons-ripple">
          <Button
            onClick={clickMapButton}
            style={buttonStyle}
            variant="link"
            size="lg"
            disabled={isMapButtonClicked}
          >
            {!isMapButtonClicked ? (
              <>Take me to the TOP!</>
            ) : (
              <>Wait for it...</>
            )}
          </Button>{" "}
        </Ripples>
        <Ripples className="Buttons-ripple">
          <Button
            onClick={clickAboutButton}
            style={buttonStyle}
            variant="link"
            size="lg"
          >
            Wait, what?
          </Button>
        </Ripples>
      </header>
    </div>
  );
}

export default Buttons;

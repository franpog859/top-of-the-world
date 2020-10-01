import React from "react";
import "./Lead.css";
import shortid from "shortid";
import { Icon } from "@iconify/react";
import bxsLockAlt from "@iconify/icons-bx/bxs-lock-alt";
import emojiSad from "@iconify/icons-heroicons-solid/emoji-sad";
import emojiHappy from "@iconify/icons-heroicons-solid/emoji-happy";

interface LeadProps {
  didFetchingFail: boolean;
  isLocationAvailable: boolean;
  isEncourageMessage: boolean;
}

function Lead({
  didFetchingFail,
  isLocationAvailable,
  isEncourageMessage
}: LeadProps) {
  const textNormal = (
    <>
      <p>
        Want to go to THE TOP OF THE WORLD but you're too lazy to even think
        about the Himalayas?
      </p>
      <p>Well, I've got something for you!</p>
    </>
  );

  const textEncourage = (
    <>
      <p>
        Want to go to THE TOP OF THE WORLD but you're too lazy to even think
        about the Himalayas?
      </p>
      <p>Well, I've got something for you!</p>
      <p>
        Just click the button <Icon icon={emojiHappy} className="Lead-icon" />
      </p>
    </>
  );

  const textNoLocation = (
    <>
      <p>Allow the location!</p>
      <p>
        Click on the <Icon icon={bxsLockAlt} className="Lead-icon" /> near the
        website address!
      </p>
    </>
  );

  const textFailedToFetch = (
    <>
      <p>
        Something went wrong <Icon icon={emojiSad} className="Lead-icon" />
      </p>
      <p>Try to refresh the app!</p>
    </>
  );

  const text = !isLocationAvailable
    ? textNoLocation
    : didFetchingFail
    ? textFailedToFetch
    : isEncourageMessage
    ? textEncourage
    : textNormal;

  // See https://stackoverflow.com/questions/57615274/my-animation-is-not-working-when-re-rending-my-react-component
  const getRandomKey = () => shortid.generate();

  return (
    <div className="Lead" data-testid="Lead">
      <div className="Lead-div Lead-animation" key={getRandomKey()}>
        {text}
      </div>
    </div>
  );
}

export default Lead;

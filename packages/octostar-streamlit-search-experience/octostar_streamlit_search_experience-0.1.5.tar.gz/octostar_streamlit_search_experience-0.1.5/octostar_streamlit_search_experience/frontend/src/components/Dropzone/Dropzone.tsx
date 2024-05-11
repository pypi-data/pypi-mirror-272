import { desktopApi, remoteAppApi } from "@octostar/platform-api";
import { DropzoneProps } from "../../types";
import classes from "./Dropzone.module.css";
import { Entity } from "@octostar/platform-types";
import { useEffect, useState } from "react";

type Props = DropzoneProps & {
  onSearchResult: (result: Entity[]) => void;
  onDropResult: (result: Entity[]) => void;
};

// const onDragStart = () => {
//   console.log("onDragStart");
// };

function Dropzone({ id, label, onDropResult, onSearchResult }: Props) {
  const [elementRef, setElementRef] = useState<HTMLElement | null>(null);

  const elementRefCallback = (element: HTMLElement | null) => {
    setElementRef(element);
  };

  useEffect(() => {
    if (!elementRef) {
      return;
    }

    // let visible = false;

    function debounce(func: (...args: unknown[]) => unknown, wait: number) {
      let timeout: number;

      return function (...args: unknown[]) {
        clearTimeout(timeout);

        timeout = setTimeout(() => func(...args), wait) as unknown as number;
      };
    }

    const updateHandler = () => {
      //   const rect = elementRef.getBoundingClientRect();
      //   const newVisible = rect.width !== 0 && rect.height !== 0;

      //   if (true || newVisible || newVisible !== visible) {
      //   visible = newVisible;
      publishDropZone();
      //   }
    };

    const debouncedUpdateHandler = debounce(updateHandler, 200); // Adjust the debounce time as needed

    const observer = new ResizeObserver((entries) => {
      entries.forEach(() => {
        debouncedUpdateHandler();
      });
    });

    observer.observe(elementRef);
    observer.observe(document.body, {
      //   childList: true,
      //   subtree: true,
      //   attributes: true,
    });

    window.addEventListener("scroll", debouncedUpdateHandler, true);

    function adjustCoordinatesForIframe(
      windowObj: Window,
      coords: {
        x: number;
        y: number;
        width: number;
        height: number;
        id: string;
      }
    ) {
      if (windowObj.parent === windowObj || !windowObj.frameElement) {
        return coords; // Base case: top-level window reached or no frameElement found
      }

      const rect = windowObj.frameElement?.getBoundingClientRect();
      // Recursive call with parent window and adjusted coordinates
      return adjustCoordinatesForIframe(windowObj.parent, {
        ...coords,
        x: coords.x + (rect?.left || 0),
        y: coords.y + (rect?.top || 0),
      });
    }

    const dropZoneId = id;

    async function publishDropZone() {
      console.log("publishDropZone");
      const rect = elementRef!.getBoundingClientRect();
      const request = adjustCoordinatesForIframe(window, {
        id: id,
        x: rect.left,
        y: rect.top,
        width: rect.width,
        height: rect.height,
      });

      //   const DROP_ZONE_REQUEST = "octostar:remoteapp:dropZoneRequest";
      //   window.parent.octostar.call(DROP_ZONE_REQUEST, request);
      console.log("dropZoneRequest", request);
      const dropResult = await remoteAppApi().dropZoneRequest([request]);

      console.log("dropZoneRequest result", dropResult);

      onDropResult(dropResult.data);
    }

    // const DRAG_START_TOPIC = "octostar:remoteapp:onDragStart";
    // window.parent.octostar.subscribe(DRAG_START_TOPIC, publishDropZone);
    console.log("Subscribe to drag events");

    remoteAppApi().subscribeToDragStart(dropZoneId, publishDropZone);

    return () => {
      observer.disconnect();
      window.removeEventListener("scroll", debouncedUpdateHandler, true);
      remoteAppApi().unsubscribeFromDragStart(dropZoneId);
    };
  }, [elementRef, id, onDropResult]);

  const handleClick = async () => {
    const searchResult = await desktopApi().searchXperience();

    onSearchResult(searchResult);
  };

  return (
    <div className={classes.root}>
      <div
        className={classes.antd_uploader}
        onClick={handleClick}
        ref={elementRefCallback}
      >
        <div className={classes.upload_icon}>+</div>
        <span className={classes.upload_text}>{label}</span>
      </div>
    </div>
  );
}

export default Dropzone;

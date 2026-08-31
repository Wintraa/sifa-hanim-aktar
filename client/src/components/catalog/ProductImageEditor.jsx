import { useCallback, useEffect, useRef, useState } from "react";
import {
  IMAGE_EDITOR_BG,
  IMAGE_EDITOR_SIZE,
  fitImageRect,
  loadImageElement,
  renderImageFrame,
} from "../../lib/imageEditor.js";

const MIN_SIDE = 36;
const HANDLES = ["nw", "n", "ne", "e", "se", "s", "sw", "w"];

function clampRect(rect) {
  return {
    x: rect.x,
    y: rect.y,
    w: Math.max(MIN_SIDE, rect.w),
    h: Math.max(MIN_SIDE, rect.h),
  };
}

function scaleRectFromCenter(rect, factor) {
  const cx = rect.x + rect.w / 2;
  const cy = rect.y + rect.h / 2;
  const w = rect.w * factor;
  const h = rect.h * factor;
  return clampRect({
    x: cx - w / 2,
    y: cy - h / 2,
    w,
    h,
  });
}

function resizeRect(rect, handle, dx, dy, lockRatio, startRect) {
  const r = { ...startRect };
  const ratio = startRect.w / startRect.h;

  if (handle.includes("e")) r.w = startRect.w + dx;
  if (handle.includes("w")) {
    r.w = startRect.w - dx;
    r.x = startRect.x + dx;
  }
  if (handle.includes("s")) r.h = startRect.h + dy;
  if (handle.includes("n")) {
    r.h = startRect.h - dy;
    r.y = startRect.y + dy;
  }

  if (lockRatio && handle.length === 2) {
    if (Math.abs(dx) >= Math.abs(dy)) {
      r.h = r.w / ratio;
      if (handle.includes("n")) r.y = startRect.y + startRect.h - r.h;
      if (handle.includes("w")) r.x = startRect.x + startRect.w - r.w;
    } else {
      r.w = r.h * ratio;
      if (handle.includes("w")) r.x = startRect.x + startRect.w - r.w;
      if (handle.includes("n")) r.y = startRect.y + startRect.h - r.h;
    }
  }

  return clampRect(r);
}

function clientToCanvas(clientX, clientY, canvas) {
  const bounds = canvas.getBoundingClientRect();
  return {
    x: ((clientX - bounds.left) / bounds.width) * IMAGE_EDITOR_SIZE,
    y: ((clientY - bounds.top) / bounds.height) * IMAGE_EDITOR_SIZE,
  };
}

/**
 * Admin ürün görseli düzenleyici — sürükle, köşeden uzat, büyüt.
 */
export function ProductImageEditor({ imageSrc, onApply, onCancel }) {
  const canvasRef = useRef(null);
  const imageRef = useRef(null);
  const fitRectRef = useRef(null);
  const dragRef = useRef(null);

  const [rect, setRect] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [lockRatio, setLockRatio] = useState(false);
  const [zoomPct, setZoomPct] = useState(100);
  const [applying, setApplying] = useState(false);
  const lockRatioRef = useRef(lockRatio);

  useEffect(() => {
    lockRatioRef.current = lockRatio;
  }, [lockRatio]);

  const onPointerMoveRef = useRef(() => {});
  const finishDragRef = useRef(() => {});

  finishDragRef.current = () => {
    dragRef.current = null;
    window.removeEventListener("pointermove", onPointerMoveRef.current);
    window.removeEventListener("pointerup", finishDragRef.current);
  };

  onPointerMoveRef.current = (e) => {
    const drag = dragRef.current;
    if (!drag) return;
    const canvas = canvasRef.current;
    if (!canvas) return;
    const point = clientToCanvas(e.clientX, e.clientY, canvas);
    const dx = point.x - drag.startX;
    const dy = point.y - drag.startY;

    if (drag.mode === "move") {
      setRect(
        clampRect({
          ...drag.startRect,
          x: drag.startRect.x + dx,
          y: drag.startRect.y + dy,
        })
      );
      return;
    }

    if (drag.mode === "resize") {
      setRect(
        resizeRect(
          drag.startRect,
          drag.handle,
          dx,
          dy,
          lockRatioRef.current,
          drag.startRect
        )
      );
    }
  };

  useEffect(
    () => () => {
      window.removeEventListener("pointermove", onPointerMoveRef.current);
      window.removeEventListener("pointerup", finishDragRef.current);
    },
    []
  );

  const redraw = useCallback((nextRect) => {
    const canvas = canvasRef.current;
    const img = imageRef.current;
    if (!canvas || !img || !nextRect) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;
    ctx.fillStyle = IMAGE_EDITOR_BG;
    ctx.fillRect(0, 0, IMAGE_EDITOR_SIZE, IMAGE_EDITOR_SIZE);
    ctx.drawImage(img, nextRect.x, nextRect.y, nextRect.w, nextRect.h);
  }, []);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError("");
    (async () => {
      try {
        const img = await loadImageElement(imageSrc);
        if (cancelled) return;
        imageRef.current = img;
        const fit = fitImageRect(img.naturalWidth, img.naturalHeight);
        fitRectRef.current = fit;
        setRect(fit);
        setZoomPct(100);
      } catch (err) {
        if (!cancelled) setError(err.message || "Görsel açılamadı.");
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [imageSrc]);

  useEffect(() => {
    redraw(rect);
  }, [rect, redraw]);

  const resetFit = () => {
    if (!fitRectRef.current) return;
    setRect({ ...fitRectRef.current });
    setZoomPct(100);
  };

  const handleZoom = (value) => {
    if (!rect || !fitRectRef.current) return;
    const factor = value / 100;
    const base = fitRectRef.current;
    const scaled = scaleRectFromCenter(base, factor);
    setZoomPct(value);
    setRect(scaled);
  };

  const startInteraction = (mode, handle, e) => {
    if (!rect) return;
    e.preventDefault();
    e.stopPropagation();
    const canvas = canvasRef.current;
    if (!canvas) return;
    const point = clientToCanvas(e.clientX, e.clientY, canvas);
    dragRef.current = {
      mode,
      handle,
      startX: point.x,
      startY: point.y,
      startRect: { ...rect },
    };
    window.addEventListener("pointermove", onPointerMoveRef.current);
    window.addEventListener("pointerup", finishDragRef.current);
  };

  const handleWheel = (e) => {
    e.preventDefault();
    if (!rect) return;
    const delta = e.deltaY > 0 ? -5 : 5;
    const next = Math.min(250, Math.max(40, zoomPct + delta));
    handleZoom(next);
  };

  const handleApply = async () => {
    if (!imageRef.current || !rect) return;
    setApplying(true);
    try {
      const dataUrl = renderImageFrame(imageRef.current, rect);
      onApply?.(dataUrl);
    } catch (err) {
      setError(err.message || "Kaydedilemedi.");
    } finally {
      setApplying(false);
    }
  };

  const frameStyle = rect
    ? {
        left: `${(rect.x / IMAGE_EDITOR_SIZE) * 100}%`,
        top: `${(rect.y / IMAGE_EDITOR_SIZE) * 100}%`,
        width: `${(rect.w / IMAGE_EDITOR_SIZE) * 100}%`,
        height: `${(rect.h / IMAGE_EDITOR_SIZE) * 100}%`,
      }
    : null;

  return (
    <div className="img-editor">
      <p className="img-editor__hint">
        Fotoğrafı sürükleyerek taşıyın; köşe ve kenarlardan çekerek uzatıp büyütün. Mouse tekerleği
        ile yakınlaştırabilirsiniz.
      </p>

      <div className="img-editor__stage">
        {loading ? <p className="img-editor__loading">Görsel yükleniyor…</p> : null}
        {error ? <p className="img-editor__error">{error}</p> : null}

        {!loading && !error && rect ? (
          <>
            <canvas
              ref={canvasRef}
              className="img-editor__canvas"
              width={IMAGE_EDITOR_SIZE}
              height={IMAGE_EDITOR_SIZE}
              onWheel={handleWheel}
            />
            <div className="img-editor__overlay">
              <div className="img-editor__frame" style={frameStyle}>
                <div
                  className="img-editor__move"
                  onPointerDown={(e) => startInteraction("move", null, e)}
                />
                {HANDLES.map((handle) => (
                  <button
                    key={handle}
                    type="button"
                    className={`img-editor__handle img-editor__handle--${handle}`}
                    aria-label={`${handle} kenarından boyutlandır`}
                    onPointerDown={(e) => startInteraction("resize", handle, e)}
                  />
                ))}
              </div>
            </div>
          </>
        ) : null}
      </div>

      <div className="img-editor__controls">
        <label className="img-editor__slider">
          <span>Büyütme</span>
          <input
            type="range"
            min="40"
            max="250"
            step="1"
            value={zoomPct}
            onChange={(e) => handleZoom(Number(e.target.value))}
          />
          <strong>{zoomPct}%</strong>
        </label>

        <label className="checkbox-field img-editor__lock">
          <input
            type="checkbox"
            checked={lockRatio}
            onChange={(e) => setLockRatio(e.target.checked)}
          />
          Oranı kilitle (köşeden çekerken)
        </label>
      </div>

      <div className="img-editor__actions">
        <button type="button" className="dropdown-link dropdown-link--button" onClick={resetFit}>
          Sığdır
        </button>
        <button type="button" className="dropdown-link dropdown-link--button" onClick={onCancel}>
          Vazgeç
        </button>
        <button
          type="button"
          className="add-product-btn"
          disabled={!rect || applying}
          onClick={handleApply}
        >
          {applying ? "Kaydediliyor…" : "Resmi Uygula"}
        </button>
      </div>
    </div>
  );
}

/** Admin girişinde vitrin üstünde görünen kısa yönlendirme. */
export function AdminPhotoHint({ isAdmin }) {
  if (!isAdmin) return null;
  return (
    <div className="admin-photo-hint" role="status">
      <strong>Admin modu açık.</strong> Her ürün fotoğrafının üstünde{" "}
      <em>Görsel Ekle</em> ve <em>Görsel Düzenle</em> butonları var — tıkla, sürükle, uzat, kaydet.
    </div>
  );
}

const ledImageModules = import.meta.glob("../../assets/leds/**/*", {
  eager: true,
  import: "default",
}) as Record<string, string>;

export const useLedImages = () => {
  const resolveLedImage = (imagePath?: string | null) => {
    if (!imagePath) {
      return "";
    }

    const normalizedPath = imagePath.replace(/^\/+/, "");
    const imageEntry = Object.entries(ledImageModules).find(([assetPath]) =>
      assetPath.endsWith(normalizedPath),
    );

    return imageEntry?.[1] ?? "";
  };

  return {
    resolveLedImage,
  };
};

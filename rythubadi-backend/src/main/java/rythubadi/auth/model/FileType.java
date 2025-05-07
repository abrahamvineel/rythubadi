package rythubadi.auth.model;

public enum FileType {
    PDF,
    IMAGE,
    WORD,
    TEXT,
    OTHER;

    public static FileType mimeType(String mimeType) {
        if (mimeType.equals("application/pdf")) {
            return PDF;
        } else if (mimeType.startsWith("image/")) {
            return IMAGE;
        } else if (mimeType.equals("application/msword") ||
                mimeType.equals("application/vnd.openxmlformats-officedocument.wordprocessingml.document")) {
            return WORD;
        } else if (mimeType.startsWith("text/")) {
            return TEXT;
        } else {
            return OTHER;
        }
    }
}

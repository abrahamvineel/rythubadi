package rythubadi.auth.model;

public enum AttachmentType {
    PDF,
    IMAGE,
    WORD,
    TEXT,
    OTHER;

    public static AttachmentType mimeType(String mimeType) {
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

package utilities
import (
  "crypto/sha512"
  "encoding/hex"
)

func GetSHA512(text string) string {
  hexHash := sha512.Sum512([]byte(text))
  return hex.EncodeToString(hexHash[:])
}

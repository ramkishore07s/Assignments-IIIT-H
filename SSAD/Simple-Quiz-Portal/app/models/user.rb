class User < ApplicationRecord
  before_save { self.email = email.downcase }
  validates :name, presence: true , length: { maximum: 50 }
  VALID_EMAIL = /\A[\w+\-.]+@[a-z\d\-]+(\.[a-z\d\-]+)*\.[a-z]+\z/i
  validates :email, presence: true , length: { maximum: 250 } , format: { with: VALID_EMAIL } , uniqueness: { case_sensitive: false }
  
  has_secure_password
  validates :password_digest, length: { minimum: 8 }

end

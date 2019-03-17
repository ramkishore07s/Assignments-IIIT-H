class Genre < ApplicationRecord
  before_save { self.subtype = subtype.downcase }
  validates :subtype, presence: true , length: { maximum: 20 }, uniqueness: true
  validates :parent, presence: true, length: { maximum: 20 }
end

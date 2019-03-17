class Touch < ApplicationRecord
  validates :genre_id, presence: true
  validates :user_id, presence: true
end

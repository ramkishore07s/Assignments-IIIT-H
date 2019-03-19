class Admin < ApplicationRecord
  validates :user_id , presence: true
end
